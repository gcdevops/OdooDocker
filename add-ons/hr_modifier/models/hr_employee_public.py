from odoo import fields, models 

class HrEmployeePublic(models.Model):
    _name= "hr.employee.public"
    _inherit = "hr.employee.public"

    parent_id = fields.Many2one(
        'hr.employee.public', 
        'Manager', 
        readonly=False,
    )