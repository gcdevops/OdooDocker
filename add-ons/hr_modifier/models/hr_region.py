# -*- coding: utf-8 -*-

from odoo import fields, models

# hr.open_view_categ_form
class HrRegion(models.Model):
    _name = "hr.region"
    _description = "Employee Region"

    name = fields.Char(string="Region Name", required = True)
    
    employee_ids = fields.One2many(
        "hr.employee",
        "region_id",
        string = "Employees"
    )

    _sql_constraints = [
        ('region_unique', 'unique (name)', 'Region already exists!')
    ]



