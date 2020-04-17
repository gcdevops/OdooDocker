from odoo import fields, models

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