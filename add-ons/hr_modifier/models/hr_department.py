# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re


class Department(models.Model):
    _name='hr.department'
    _inherit='hr.department'
    name = fields.Char('Department Name', required=True, translate = True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True, translate=True)
    x_coordinators_ids = fields.Many2many('hr.employee', 'hr_department_coordinator_rel', 'dept', 'employee', string='Coordinators')

    @api.onchange("x_coordinators_ids")
    def _onchange_coordinator(self):
        [ self.env[i].clear_caches() for i in self.env ]
    
    # Validation

    # allow upper case, lower case, hyphens
    @api.constrains("name")
    def _check_name_allowed_characters(self):
        for record in self:
            if record.name:
                res = re.search(r"[^\w\d\s\-.,'&/()@]", record.name)
                if res:
                    raise ValidationError("The department name contains an invalid character: " + res.group(0))