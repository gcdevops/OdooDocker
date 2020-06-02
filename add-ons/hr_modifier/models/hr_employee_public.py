from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re

class HrEmployeePublic(models.Model):
    _name= "hr.employee.public"
    _inherit = "hr.employee.public"
    x_employee_language = fields.Selection(readonly = True)

    x_employee_job_type = fields.Char(readonly = True)
    
    x_employee_status = fields.Selection(readonly = True)

    x_employee_access_gov_office = fields.Boolean(readonly=True)
    
    x_employee_device_type = fields.Selection(readonly=True)

    x_employee_asset_number = fields.Char(readonly=True)
    
    x_employee_office_floor = fields.Char(readonly=True)
    
    x_employee_office_cubicle = fields.Char(readonly=True)

    x_employee_is_remote = fields.Boolean(readonly=True)

    x_employee_second_monitor = fields.Boolean(readonly=True)

    x_employee_mobile_hotspot = fields.Boolean(readonly=True)

    x_employee_headset = fields.Boolean(readonly=True)

    classification_id = fields.Many2one(readonly=True)

    region_id = fields.Many2one(readonly=True)

    branch_id = fields.Many2one(readonly=True)

    x_employee_remote_access_network = fields.Boolean(readonly=True)

    x_employee_remote_access_tool = fields.Selection(readonly = True)

    parent_id = fields.Many2one(
        'hr.employee.public', 
        'Manager', 
        readonly=False,
    )
