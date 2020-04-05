# -*- coding: utf-8 -*-

from odoo import fields, models

# hr.open_view_categ_form
class HrClassification(models.Model):
    _name = "hr.classification"
    _description = "Employee Classification"

    name = fields.Char(string="Classification Name", required = True)
    level = fields.Integer(string="Level", required = True)
    employee_ids = fields.One2many(
        "hr.employee",
        "classification_id",
        string = "Employees"
    )

    _sql_constraints = [
        ('class_unique', 'unique (name,level)', 'Classification already exists !')
    ]

    def name_get(self):
        if self.env.context.get("name_only", False):
            return super(HrClassification, self).name_get()
        return [(record.id, record.name + "-" + str(record.level)) for record in self]

