# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re


class Department(models.Model):
    _name='hr.department'
    _inherit='hr.department'
    parent_id = fields.Many2one(string='Parent Team')
    name = fields.Char('Team Name', required=True, translate = True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=False, translate=True)
    x_coordinators_ids = fields.Many2many('hr.employee', 'hr_department_coordinator_rel', 'dept', 'employee', string='Coordinators')
    # x_reporter_ids = fields.Many2many('hr.employee', 'hr_department_reporter_rel', 'dept', 'employee', string='Reporters')

    @api.onchange("x_coordinators_ids")
    def _onchange_coordinator(self):
        [ self.env[i].clear_caches() for i in self.env ]

    # @api.onchange("x_reporter_ids")
    # def _onchange_reporter(self):
    #     [ self.env[i].clear_caches() for i in self.env ]
    
    # Validation

    # allow upper case, lower case, hyphens
    @api.constrains("name")
    def _check_name_allowed_characters(self):
        for record in self:
            if record.name:
                res = re.search(r"[^\w\d\s\-.,'&/()@]", record.name)
                if res:
                    raise ValidationError("The team name contains an invalid character: " + res.group(0))