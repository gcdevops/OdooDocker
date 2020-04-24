from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class HrJob(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    #name = fields.Char(string="Region Name", required = True)

    #  Validation

    # allow [a-zA-Z0-9 -]
    @api.constrains("name")
    def _check_alpha_numeric_space_dash(self):
        for record in self:
            res = re.search("[a-zA-Z0-9 -]", record.job_id)
            if not res:
                raise ValidationError("The job title can only contain letters, numbers, spaces, and hyphens")