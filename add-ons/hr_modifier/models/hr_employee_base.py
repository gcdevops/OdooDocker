from odoo import fields, models

class HrEmployeeBase(models.AbstractModel):
    _name = "hr.employee.base"
    _inherit = "hr.employee.base"

    x_employee_work_criticality = fields.Boolean("Work criticality")
    x_employee_level_criticality = fields.Selection(
        [
            ("1", "1 - Call centres"),
            ("2", "2 - Claims processing"),
            ("3", "3 - Others")
        ],
        string = "Level of criticality"
    )
    x_employee_language = fields.Selection(
        [
            ("english", "English"),
            ("french", "French"),
            ("bilingual", "Bilingual")
        ],
        string = "Language"
    )
    