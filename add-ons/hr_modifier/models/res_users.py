from odoo import models, fields, api

class Users(models.Model):
    _inherit = 'res.users'
    odoobot_state = fields.Selection(default="disabled")
    x_department_coordinators_ids = fields.Many2many(
        related='employee_id.x_department_coordinators_ids',
        string = "Departments Coordinating",
        readonly=False,
        related_sudo=False
    )
    
    @api.onchange("x_department_coordinators_ids")
    def _onchange_coordinator(self):
        self.env['ir.rule'].clear_caches()