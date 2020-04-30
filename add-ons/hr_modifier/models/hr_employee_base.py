from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import json

class HrEmployeeBase(models.AbstractModel):
    _name = "hr.employee.base"
    _inherit = "hr.employee.base"

    x_employee_language = fields.Selection(
        [
            ("english", "English"),
            ("french", "French"),
            ("bilingual", "Bilingual")
        ],
        string = "Language"
    )

    x_employee_job_type = fields.Char("Job type", groups="hr.group_hr_user")

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
    
    x_employee_status = fields.Selection(
        [
            ("contractor", "Contractor"),
            ("casual", "Casual"),
            ("indeterminate", "Indeterminate"),
            ("term", "Term"),
            ("assignment", "Assignment"),
            ("student", "Student")
        ],
        groups = "hr.group_hr_user",
        string = "Employment status"
    )

    x_employee_access_gov_office = fields.Boolean("Access to a government office", groups="hr.group_hr_user")
    
    x_employee_device_type = fields.Selection(
        [
            ("laptop", "Laptop"),
            ("desktop", "Desktop"),
            ("tablet", "Tablet")
        ],
        groups = "hr.group_hr_user",
        string = "Device type"
    )

    x_employee_asset_number = fields.Char(
        "Asset number",
        groups = "hr.group_hr_user"
    )
    
    x_employee_office_floor = fields.Char(
        "Office floor",
        groups = "hr.group_hr_user"
    )
    
    x_employee_office_cubicle = fields.Char(
        "Office cubicle",
        groups = "hr.group_hr_user"
    )
    x_employee_is_remote = fields.Boolean(
        "Remote employee",
        groups = "hr.group_hr_user"
    )

    x_employee_second_monitor = fields.Boolean(
        "Second monitor availability",
        groups="hr.group_hr_user"
    )

    x_employee_mobile_hotspot = fields.Boolean(
        "Mobile hotspot availability",
        groups = "hr.group_hr_user"
    )

    x_employee_headset = fields.Boolean(
        "Headset availability",
        groups = "hr.group_hr_user"
    )

    classification_id = fields.Many2one(
        "hr.classification",
        ondelete = "set null"
    )

    region_id = fields.Many2one(
        "hr.region",
        ondelete = "set null"
    )

    x_employee_remote_access_network = fields.Boolean(
        "Remote access to network",
        groups = "hr.group_hr_user"
    )

    x_employee_remote_access_tool = fields.Selection(
        [
            ('both', "Both"),
            ("vpn", "VPN"),
            ("appgate", "AppGate")
        ],
        groups = "hr.group_hr_user",
        string = "Remote connection tool"
    )
    address_id = fields.Many2one('res.partner', 'Work Address', domain="['&', '|', ('company_id', '=', False), ('company_id', '=', company_id), ('is_company', '=', True)]")

    # Validation

    
    
    # if special characters are found, raise an error
    @api.constrains("work_email")
    def _check_work_email_allowed_characters(self):
        for record in self:
            if record.work_email:
                if re.search(r"['\"*?;/\\]", record.work_email):
                    raise ValidationError("The work email is invalid")


    # allow upper case, lower case, hyphens
    @api.constrains("name")
    def _check_name_allowed_characters(self):
        for record in self:
            if record.name:
                res = re.search("[^a-zA-Z\s\-,.''.À-Öà-ö]", record.name)
                if res:
                    raise ValidationError("The employee name contains an invalid character: " + res.group(0))