from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class HrJob(models.Model):
    _name = "hr.job"
    _inherit = "hr.job"

    #  Validation

    # allow upper case, lower case, hyphens, digits, spaces
    @api.constrains("name")
    def _check_name_allowed_characters(self):
        for record in self:
            if record.name:
                res = re.search("[^a-zA-Z\d\s:\-,\(\)/&.@À-Öà-ö]", record.name)
                if res:
                    raise ValidationError("The job position contains an invalid character: " + res.group(0))