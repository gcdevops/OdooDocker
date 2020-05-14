from odoo import models, fields

class Users(models.Model):
    _inherit = 'res.users'
    odoobot_state = fields.Selection(default="disabled")
    x_department_coordinators_ids = fields.Many2many(
        related="employee_id.x_department_coordinators_ids",
        string="Teams Coordinating",
        readonly=False,
        related_sudo=False
    )
    # x_department_reporter_ids = fields.Many2many(
    #     related="employee_id.x_department_reporter_ids",
    #     string="Teams reporting",
    #     readonly=False,
    #     related_sudo=False
    # )