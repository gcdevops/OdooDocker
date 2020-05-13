# -*- coding: utf-8 -*-

from odoo import fields, models

# hr.open_view_categ_form
class HrBranch(models.Model):
    _name = "hr.branch"
    _description = "BRM Branch"

    name = fields.Char(string="Name", required = True, translate = True)
    
    employee_ids = fields.One2many(
        "hr.employee",
        "branch_id",
        string = "Employees"
    )

    _sql_constraints = [
        ('branch_unique', 'unique (name)', 'Branch already exists!')
    ]