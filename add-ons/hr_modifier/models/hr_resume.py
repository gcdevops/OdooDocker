# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class Employee(models.Model):
    _inherit = 'hr.employee'

    employee_skill_ids = fields.One2many(string="Profile")

