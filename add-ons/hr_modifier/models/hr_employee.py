from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrEmployeePrivate(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    x_employee_personal_home_address = fields.Char(
        "Home address",
        groups = "hr.group_hr_user"
    )

    x_employee_personal_postal_code = fields.Char(
        "Postal code",
        groups = "hr.group_hr_user"
    )
    x_employee_personal_phone = fields.Char(
        "Personal phone number",
        groups = "hr.group_hr_user"
    )
    x_employee_personal_email = fields.Char(
        "Personal email",
        groups = "hr.group_hr_user"
    )

    x_employee_pri = fields.Char("Employee PRI", groups="hr.group_hr_user")
    
    x_employee_job_code = fields.Char("Job code", groups="hr.group_hr_user")
    
    x_employee_job_type = fields.Char("Job type", groups="hr.group_hr_user")
    
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
    
    x_employee_remote_access_network = fields.Boolean(
        "Remote access to network",
        groups = "hr.group_hr_user"
    )

    x_employee_remote_access_tool = fields.Selection(
        [
            ("vpn", "VPN"),
            ("appgate", "AppGate")
        ],
        groups = "hr.group_hr_user",
        string = "Remote connection tool"
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
        if self.region_id != self.parent_id.region_id and self.parent_id.region_id is not None:
            self.region_id = self.parent_id.region_id