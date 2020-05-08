# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re

class Skill(models.Model):
    _name = 'hr.skill'
    _inherit='hr.skill'

    name = fields.Char(translate = True)

class SkillType(models.Model):
    _name = 'hr.skill.type'
    _inherit='hr.skill.type'

    name = fields.Char(translate = True)
    skill_ids = fields.One2many(string="Enabling Services")

class EmployeeSkill(models.Model):
    _name = 'hr.employee.skill'
    _inherit = 'hr.employee.skill'
    _order = "skill_type_id"


    skill_id = fields.Many2one(string="Profiles")
    skill_level_id = fields.Many2one(required=False)

    def _check_skill_level(self):
        return True
