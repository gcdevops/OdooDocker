# -*- coding: utf-8 -*-

from odoo import fields, models

# hr.open_view_categ_form
class ResBuildingType(models.Model):
    _name = "res.building_type"
    _description = "Building Type"

    name = fields.Char(string="Name", required = True, translate = True)

    _sql_constraints = [
        ('building_type_unique', 'unique (name)', 'Building Type already exists!')
    ]