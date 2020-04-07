from odoo import fields, models

class HrEmployeeBase(models.AbstractModel):
    _name = "hr.employee.base"
    _inherit = "hr.employee.base"

    x_employee_work_criticality = fields.Boolean("Work criticality")

    x_employee_language = fields.Selection(
        [
            ("english", "English"),
            ("french", "French"),
            ("bilingual", "Bilingual")
        ],
        string = "Language"
    )
    