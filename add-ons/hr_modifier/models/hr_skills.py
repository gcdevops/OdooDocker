# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re

class SkillType(models.Model):
    _name = 'hr.skill.type'
    _inherit='hr.skill.type'

    skill_ids = fields.One2many(string="Enabling Services")

    # Validation

    # allow upper case, lower case, hyphens
    @api.constrains("name")
    def _check_name_allowed_characters(self):
        for record in self:
            if record.name:
                res = re.search("[^a-zA-Z\s\- \.]", record.name)
                if res:
                    raise ValidationError("The enabling service name contains an invalid character: " + res.group(0))

class EmployeeSkill(models.Model):
    _name = 'hr.employee.skill'
    _inherit = 'hr.employee.skill'

    skill_id = fields.Many2one(string="Profiles")

    # Validation

    # allow upper case, lower case, hyphens
    @api.constrains("name")
    def _check_name_allowed_characters(self):
        for record in self:
            if record.name:
                res = re.search("[^a-zA-Z\s\- \.]", record.name)
                if res:
                    raise ValidationError("The profile name contains an invalid character: " + res.group(0))