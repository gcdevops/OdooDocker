# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _
import re
from odoo.exceptions import AccessError
from odoo.http import request

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Normal'),
    ('2', 'High'),
    ('3', 'Urgent'),
]


class HelpdeskTicket(models.Model):
    _name = "helpdesk_lite.ticket"
    _description = "Helpdesk Ticket"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = "priority desc, create_date desc"
    _mail_post_access = 'read'

    @api.model
    def _get_default_stage_id(self):
        return self.env['helpdesk_lite.stage'].search([], order='sequence', limit=1)

    name = fields.Char(string='Ticket', track_visibility='always', required=True)
    description = fields.Text(string='Description')
    partner_id = fields.Many2one('res.partner', string='Employee', track_visibility='onchange', index=True, default=lambda self: self.env.user.partner_id)
    commercial_partner_id = fields.Many2one(
        related='partner_id.commercial_partner_id', string='Customer Company', store=True, index=True)
    contact_name = fields.Char('Contact Name')
    email_from = fields.Char('Email', help="Email address of the contact", index=True)
    user_id = fields.Many2one('res.users', string='Assigned to', track_visibility='onchange', index=True, default=False)
    team_id = fields.Many2one('helpdesk_lite.team', string='Support Team', track_visibility='onchange',
        default=lambda self: self.env['helpdesk_lite.team'].sudo()._get_default_team_id(user_id=self.env.uid),
        index=True, help='When sending mails, the default email address is taken from the support team.')
    date_deadline = fields.Datetime(string='Deadline', track_visibility='onchange')
    date_done = fields.Datetime(string='Done', track_visibility='onchange')

    stage_id = fields.Many2one('helpdesk_lite.stage', string='Status', index=True, track_visibility='onchange',
                               domain="[]",
                               copy=False,
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id)
    priority = fields.Selection(AVAILABLE_PRIORITIES, 'Priority', index=True, default='1', track_visibility='onchange')
    kanban_state = fields.Selection([('normal', 'Normal'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
                                    string='Kanban State', track_visibility='onchange',
                                    required=True, default='normal',
                                    help="""A Ticket's kanban state indicates special situations affecting it:\n
                                           * Normal is the default situation\n
                                           * Blocked indicates something is preventing the progress of this ticket\n
                                           * Ready for next stage indicates the ticket is ready to go to next stage""")

    color = fields.Integer('Color Index')
    legend_blocked = fields.Char(related="stage_id.legend_blocked", readonly=True)
    legend_done = fields.Char(related="stage_id.legend_done", readonly=True)
    legend_normal = fields.Char(related="stage_id.legend_normal", readonly=True)

    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """ This function sets partner email address based on partner
        """
        self.email_from = self.partner_id.email

    def copy(self, default=None):
        if default is None:
            default = {}
        default.update(name=_('%s (copy)') % (self.name))
        return super(HelpdeskTicket, self).copy(default=default)

    def _can_add__recipient(self, partner_id):
        if not self.partner_id.email:
            return False
        if self.partner_id in self.message_follower_ids.mapped('partner_id'):
            return False
        return True

    def message_get_suggested_recipients(self):
        recipients = super(HelpdeskTicket, self).message_get_suggested_recipients()
        try:
            for tic in self:
                if tic.partner_id:
                    if tic._can_add__recipient(tic.partner_id):
                        tic._message_add_suggested_recipient(recipients, partner=tic.partner_id,
                                                             reason=_('Customer'))
                elif tic.email_from:
                    tic._message_add_suggested_recipient(recipients, email=tic.email_from,
                                                         reason=_('Customer Email'))
        except AccessError:  # no read access rights -> just ignore suggested recipients because this imply modifying followers
            pass
        return recipients

    def _email_parse(self, email):
        match = re.match(r"(.*) *<(.*)>", email)
        if match:
            contact_name, email_from =  match.group(1,2)
        else:
            match = re.match(r"(.*)@.*", email)
            contact_name =  match.group(1)
            email_from = email
        return contact_name, email_from

    @api.model
    def message_new(self, msg, custom_values=None):
        match = re.match(r"(.*) *<(.*)>", msg.get('from'))
        if match:
            contact_name, email_from =  match.group(1,2)
        else:
            match = re.match(r"(.*)@.*", msg.get('from'))
            contact_name =  match.group(1)
            email_from = msg.get('from')

        body = tools.html2plaintext(msg.get('body'))
        bre = re.match(r"(.*)^-- *$", body, re.MULTILINE|re.DOTALL|re.UNICODE)
        desc = bre.group(1) if bre else None

        defaults = {
            'name':  msg.get('subject') or _("No Subject"),
            'email_from': email_from,
            'description':  desc or body,
        }

        partner = self.env['res.partner'].sudo().search([('email', '=ilike', email_from)], limit=1)
        if partner:
            defaults.update({
                'partner_id': partner.id,
            })
        else:
            defaults.update({
                'contact_name': contact_name,
            })

        create_context = dict(self.env.context or {})
        # create_context['default_user_id'] = False
        # create_context.update({
        #     'mail_create_nolog': True,
        # })

        company_id = False
        if custom_values:
            defaults.update(custom_values)
            team_id = custom_values.get('team_id')
            if team_id:
                team = self.env['helpdesk_lite.team'].sudo().browse(team_id)
                if team.company_id:
                    company_id = team.company_id.id
        if not company_id and partner.company_id:
            company_id = partner.company_id.id
        defaults.update({'company_id': company_id})

        return super(HelpdeskTicket, self.with_context(create_context)).message_new(msg, custom_values=defaults)

    @api.model_create_single
    def create(self, vals):
        context = dict(self.env.context)
        context.update({
            'mail_create_nosubscribe': False,
        })

        res = super(HelpdeskTicket, self.with_context(context)).create(vals)
        # res = super().create(vals)
        if res.partner_id:
            res.message_subscribe([res.partner_id.id])

        support_ticket_menu = request.env['ir.model.data'].sudo().get_object('hr', 'menu_hr_root')
        support_ticket_action = request.env['ir.model.data'].sudo().get_object('helpdesk_lite', 'helpdesk_ticket_manager_list_act')
        url = request.httprequest.host_url + "web#id=" + str(res.id)  + "&view_type=form&model=helpdesk_lite.ticket&menu_id=" + str(support_ticket_menu.id) + "&action=" + str(support_ticket_action.id)

        body_html = '''\
        <p>New ticket #{ticket_id} for HR WhiteListing:</p>
        <p><b>{name}</b></p>
        <p>{body}</p>
        <p>Click <a href="{url}">here</a> to view the ticket and reply.</p>
        <p>Thank you</p>
        <hr>
        <p>Nouveau billet #{ticket_id} de l'application RH WhiteListing :</p>
        <p><b>{name}</b></p>
        <p>{body}</p>
        <p>Cliquez <a href="{url}">ici</a> pour voir le billet et répondre.</p>
        <p>Merci</p>
        \
        '''.format(ticket_id=res.id, name=res.name, body=res.description, url=url)

        #Send email
        values = dict(
            body_html=body_html,
            email_to=res.company_id.administration_email,
            email_from="noreply@grh-hrm.iitb-dgiit.ca",
            subject="New ticket #" + str(res.id)  + " for HR WhiteListing | Nouveau billet #" + str(res.id)  + " pour RH WhiteListing"
        )

        send_mail = self.env['mail.mail'].create(values)
        send_mail.send()

        body_html = '''\
        <p>Ticket #{ticket_id} created for HR WhiteListing:</p>
        <p><b>{name}</b></p>
        <p>{body}</p>
        <p>Click <a href="{url}">here</a> to view your ticket.</p>
        <p>Thank you</p>
        <hr>
        <p>Nouveau billet #{ticket_id} créé pour l'application RH WhiteListing :</p>
        <p><b>{name}</b></p>
        <p>{body}</p>
        <p>Cliquez <a href="{url}">ici</a> pour voir votre billet.</p>
        <p>Merci</p>
        \
        '''.format(ticket_id=res.id, name=res.name, body=res.description, url=url)

        #Send email
        values = dict(
            body_html=body_html,
            email_to=res.email_from,
            email_from="noreply@grh-hrm.iitb-dgiit.ca",
            subject="Ticket #" + str(res.id)  + " for HR WhiteListing | Billet #" + str(res.id)  + " pour RH WhiteListing"
        )

        send_mail = self.env['mail.mail'].create(values)
        send_mail.send()

        return res

    def write(self, vals):
        # stage change: update date_last_stage_update
        if 'stage_id' in vals:
            if 'kanban_state' not in vals:
                vals['kanban_state'] = 'normal'
            stage = self.env['helpdesk_lite.stage'].browse(vals['stage_id'])
            if stage.last:
                vals.update({'date_done': fields.Datetime.now()})
            else:
                vals.update({'date_done': False})

        return super(HelpdeskTicket, self).write(vals)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):

        search_domain = []

        # perform search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def takeit(self):
        self.ensure_one()
        vals = {
            'user_id' : self.env.uid,
            # 'team_id': self.env['helpdesk_lite.team'].sudo()._get_default_team_id(user_id=self.env.uid).id
        }
        return super(HelpdeskTicket, self).write(vals)

    def _register_hook(self):
        HelpdeskTicket.website_form = bool(self.env['ir.module.module'].
        search([('name', '=', 'website_form'), ('state', '=', 'installed')]))
        if HelpdeskTicket.website_form:
            self.env['ir.model'].search([('model', '=', self._name)]).write({'website_form_access': True})
            self.env['ir.model.fields'].formbuilder_whitelist(
                self._name, ['name', 'description', 'date_deadline', 'priority', 'partner_id', 'user_id'])
        pass


class WebsiteSupportTicketCompose(models.Model):

    _name = "helpdesk_lite.ticket.compose"

    body = fields.Text(string="Message Body")
    name = fields.Char(string='Ticket', readonly="True")
    ticket_id = fields.Many2one('helpdesk_lite.ticket', string='Ticket ID', readonly="True")
    partner_id = fields.Many2one('res.partner', string="Partner", readonly="True")
    email_from = fields.Char(string="Email", readonly="True")
    user_id = fields.Many2one('res.users', string='Assigned to')

    def send_reply_manager(self):

        support_ticket_menu = request.env['ir.model.data'].sudo().get_object('hr', 'menu_hr_root')
        support_ticket_action = request.env['ir.model.data'].sudo().get_object('helpdesk_lite', 'helpdesk_ticket_manager_list_act')
        url = request.httprequest.host_url + "web#id=" + str(self.ticket_id.id) + "&view_type=form&model=helpdesk_lite.ticket&menu_id=" + str(support_ticket_menu.id) + "&action=" + str(support_ticket_action.id)

        body_html = '''\
        <p>New reply to HR WhiteListing Ticket #{ticket_id}:</p>
        <p><b>{name}</b></p>
        <p>{body}</p>
        <p>Click <a href="{url}">here</a> to view your ticket and reply.</p>
        <p>Thank you</p>
        <hr>
        <p>Nouvelle réponse à votre billet #{ticket_id} de l'application RHWhiteListing :</p>
        <p><b>{name}</b></p>
        <p>{body}</p>
        <p>Cliquez <a href="{url}">ici</a> pour voir votre billet et répondre.</p>
        <p>Merci</p>
        \
        '''.format(ticket_id=str(self.ticket_id.id), name=self.name, body=self.body, url=url)

        #Send email
        values = dict(
            body_html=body_html,
            email_to=self.email_from,
            email_from="noreply@grh-hrm.iitb-dgiit.ca",
            subject="Reply to HR WhiteListing Ticket #" + str(self.ticket_id.id) + " | Réponse au billet #"  + str(self.ticket_id.id) + " de RH WhiteListing"
        )

        send_mail = self.env['mail.mail'].create(values)
        send_mail.send()

        self.ticket_id.message_post(body=self.body, message_type='email', subtype='mt_comment')

    def send_reply_user(self):

        support_ticket_menu = request.env['ir.model.data'].sudo().get_object('hr', 'menu_hr_root')
        support_ticket_action = request.env['ir.model.data'].sudo().get_object('helpdesk_lite', 'helpdesk_ticket_manager_list_act')
        url = request.httprequest.host_url + "web#id=" + str(self.ticket_id.id) + "&view_type=form&model=helpdesk_lite.ticket&menu_id=" + str(support_ticket_menu.id) + "&action=" + str(support_ticket_action.id)

        body_html = '''\
        <p>New reply to HR WhiteListing Ticket #{ticket_id}:</p>
        <p><b>{name}</b></p>
        <p>{body}</p>
        <p>Click <a href="{url}">here</a> to view your ticket and reply.</p>
        <p>Thank you</p>
        <hr>
        <p>Nouvelle réponse à votre billet #{ticket_id} de l'application RH WhiteListing :</p>
        <p><b>{name}</b></p>
        <p>{body}</p>
        <p>Cliquez <a href="{url}">ici</a> pour voir votre billet et répondre.</p>
        <p>Merci</p>
        \
        '''.format(ticket_id=str(self.ticket_id.id), name=self.name, body=self.body, url=url)

        #Send email
        values = dict(
            body_html=body_html,
            email_to=self.user_id.email,
            email_from="noreply@grh-hrm.iitb-dgiit.ca",
            subject="Reply to HR WhiteListing Ticket #" + str(self.ticket_id.id) + " | Réponse au billet #"  + str(self.ticket_id.id) + " de RH WhiteListing"
        )

        send_mail = self.env['mail.mail'].create(values)
        send_mail.send()

        self.ticket_id.message_post(body=self.body, message_type='email', subtype='mt_comment')