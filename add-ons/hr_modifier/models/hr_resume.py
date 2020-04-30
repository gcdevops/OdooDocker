# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class Employee(models.Model):
    _inherit = 'hr.employee'

    employee_skill_ids = fields.One2many(string="Profile")

    #  Validation

    # allow upper case, lower case, hyphens, digits, spaces
    @api.constrains("name")
    def _check_name_allowed_characters(self):
        for record in self:
            if record.name:
                res = re.search("[^a-zA-Z\d\s:\-,\(\)/&.@À-Öà-ö]", record.name)
                if res:
                    raise ValidationError("The resume name contains an invalid character: " + res.group(0))