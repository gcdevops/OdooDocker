from odoo import models, fields

class Users(models.Model):
    _inherit = 'res.users'
    odoobot_state = fields.Selection(default="disabled")
    x_department_coordinators_ids = fields.Many2many('hr.department', 'hr_department_coordinator_rel', 'employee', 'dept')