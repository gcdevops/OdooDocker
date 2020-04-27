from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class HrJob(models.Model):
    _name = "hr.job"
    _inherit = "hr.job"

    #  Validation

    # allow [a-zA-Z0-9 -]
    @api.constrains("name")
    def _check_alpha_numeric_space_dash(self):
        for record in self:
            if re.search("[^a-zA-Z\d\s:\-,]", record.name):
                raise ValidationError("The job position can only contain letters, numbers, spaces, commas, and hyphens")