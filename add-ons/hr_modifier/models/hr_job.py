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
                if re.search("[^a-zA-Z\d\s:\-,]", record.name):
                    raise ValidationError("The job position can only contain letters, numbers, spaces, commas, and hyphens")