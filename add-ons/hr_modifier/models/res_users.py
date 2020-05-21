from odoo import models, fields

class Users(models.Model):
    _inherit = 'res.users'
    odoobot_state = fields.Selection(default="disabled")
    notification_type = fields.Selection(default='inbox')
    x_department_coordinators_ids = fields.Many2many(
        related="employee_id.x_department_coordinators_ids",
        string="Teams Coordinating",
        readonly=False,
        related_sudo=False
    )