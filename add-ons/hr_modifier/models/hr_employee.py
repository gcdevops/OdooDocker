from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re



class HrEmployeePrivate(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    x_department_coordinators_ids = fields.Many2many('hr.department', 'hr_department_coordinator_rel', 'employee', 'dept')

    x_department_reporter_ids = fields.Many2many('hr.department', 'hr_department_reporter_rel', 'employee', 'dept')

    x_employee_work_criticality = fields.Boolean("Work criticality")


    # DEPRECIATED 
    x_employee_personal_home_address = fields.Char(
        "Home address",
        groups = "hr.group_hr_user"
    )

    # DEPRECIATED 
    x_employee_personal_postal_code = fields.Char(
        "Postal code",
        groups = "hr.group_hr_user"
    )

    # DEPRECIATED 
    x_employee_personal_phone = fields.Char(
        "Personal phone number",
        groups = "hr.group_hr_user"
    )

    # DEPRECIATED 
    x_employee_personal_email = fields.Char(
        "Personal email",
        groups = "hr.group_hr_user"
    )

    # DEPRECIATED 
    x_employee_pri = fields.Char("Employee PRI", groups="hr.group_hr_user")
    
    x_employee_job_code = fields.Char("Job code", groups="hr.group_hr_user")
    
    _sql_constraints = [
        ('barcode_uniq', 'unique (barcode)', "The Badge ID must be unique, this one is already assigned to another employee."),
        ('user_uniq', 'unique (user_id, company_id)', "A user cannot be linked to multiple employees in the same company."),
        ("pri_uniq", 'unique (x_employee_pri)', "The Employee PRI must be unique, this one is already assigned to another employee")
    ]
    
    @api.onchange("parent_id")
    def _onchange_manager(self):
        if self.region_id != self.parent_id.region_id:
            self.region_id = self.parent_id.region_id
    
    # Validation

    # check if employee pri is an integer
    @api.constrains("x_employee_pri")
    def _check_employee_pri(self):
        for record in self:
            try:
                int(record.x_employee_pri)
            except:
                raise ValidationError("Employee PRI must be a number")
    
    
    
