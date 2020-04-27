from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class HrJob(models.Model):
    #_name = "hr.job"
    _inherit = "hr.job"

    name = fields.Char(string="Region Name", required = True)

    #  Validation

    # allow [a-zA-Z0-9 -]
    @api.constrains("name")
    def _check_alpha_numeric_space_dash(self):
        for record in self:
            res = re.match("[^[\w -]+$", record.name)
            if res:
                raise ValidationError("The job position can only contain letters, numbers, spaces, and hyphens: ", res)
            else:
                raise ValidationError("The job title matches: ", res)