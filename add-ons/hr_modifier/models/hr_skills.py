# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re

class SkillType(models.Model):
    _name = 'hr.skill.type'
    _inherit='hr.skill.type'

    skill_ids = fields.One2many(string="Enabling Services")


class EmployeeSkill(models.Model):
    _name = 'hr.employee.skill'
    _inherit = 'hr.employee.skill'

    skill_id = fields.Many2one(string="Profiles")
