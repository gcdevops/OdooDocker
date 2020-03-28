# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Department(models.Model):
    _name='hr.department'
    _inherit='hr.department'
    name = fields.Char('Department Name', required=True, translate = True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True, translate=True)

   