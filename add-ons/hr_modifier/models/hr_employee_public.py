from odoo import models, fields 

class HrEmployeePublic(models.Model):
    _name= "hr.employee.public"
    _inherit= "hr.employee.public"

    x_employee_work_criticality = fields.Boolean(readonly=True)
    x_employee_level_criticality = fields.Selection(readonly=True)
