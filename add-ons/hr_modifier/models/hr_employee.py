from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json
import logging

logger = logging.getLogger(__name__)


class HrEmployeePrivate(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    x_department_coordinators_ids = fields.Many2many('hr.department', 'hr_department_coordinator_rel', 'employee', 'dept')

    x_employee_work_criticality = fields.Boolean("Work criticality")

    department_id_domain = fields.Char(
        compute = "_compute_department_id_domain",
        readonly = True,
        store = False 
    )

    parent_id_domain = fields.Char(
        compute = "_compute_parent_id_domain",
        readonly = True,
        store = False
    )

    @api.depends("department_id")
    def _compute_department_id_domain(self):
         # get the current user groups
        current_user = self.env.user 
        current_user_groups = list(map(lambda x: x.name, current_user.groups_id))

        # if Senior Management or Coordinator is in the user groups, return the restricted domain

        for rec in self: 
            if("Senior Management" in current_user_groups or "Coordinator" in current_user_groups):
                rec.department_id_domain = json.dumps(
                    ['|', ('id', 'child_of', [
                            employee.department_id.id for employee in current_user.employee_ids
                        ]), ('id','child_of',[ 
                            department.id for department in current_user.x_department_coordinators_ids
                    ])]
                )
            else:
                rec.department_id_domain = json.dumps([("active", "=", True)])
    
    @api.depends("parent_id")
    def _compute_parent_id_domain(self):
        # get the current user groups
        current_user = self.env.user 
        current_user_groups = list(map(lambda x: x.name, current_user.groups_id))

        # if Senior Management or Coordinator is in the user groups, return the restricted domain

        for rec in self: 
            if("Senior Management" in current_user_groups or "Coordinator" in current_user_groups):
                rec.parent_id_domain = json.dumps(
                    ['|', ('id', 'child_of', [
                        employee.id for employee in current_user.employee_ids
                    ]), ('department_id', 'child_of', [
                        department.id for department in current_user.x_department_coordinators_ids
                    ])]
                )
            else:
                rec.parent_id_domain = json.dumps([("active", "=", True)])



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

    # check if employee pri is an integer
    @api.constrains("x_employee_pri")
    def _check_employee_pri(self):
        for record in self:
            try:
                int(record.x_employee_pri)
            except:
                raise ValidationError("Employee PRI must be a number")
    
    @api.onchange("parent_id")
    def _onchange_manager(self):
        if self.region_id != self.parent_id.region_id:
            self.region_id = self.parent_id.region_id
    """
    @api.onchange("user_partner_id")
    def _onchange_department(self):
        # get the current user groups
        current_user = self.env.user 
        current_user_groups = list(map(lambda x: x.name, current_user.groups_id))

        # if Senior Management or Coordinator is in the user groups, return the restricted domain 
        if("Senior Management" in current_user_groups or "Coordinator" in current_user_groups):
            return {
                "domain": {
                    "department_id": ['|', ('id', 'child_of', [
                        employee.department_id.id for employee in current_user.employee_ids
                    ]), ('id','child_of',[ 
                        department.id for department in current_user.x_department_coordinators_ids
                    ])],
                    "parent_id": ['|', ('id', 'child_of', [
                        employee.id for employee in current_user.employee_ids
                    ]), ('department_id', 'child_of', [
                        department.id for department in current_user.x_department_coordinators_ids
                    ])]
                }
            }
    """
        




