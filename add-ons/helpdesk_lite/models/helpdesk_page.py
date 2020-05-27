# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools.translate import html_translate

class HelpdeskPage(models.Model):

    _name = "helpdesk_lite.page"
    _order = "name asc"

    name = fields.Char(string='Name', translate=True)
    content = fields.Html(sanitize=False, string='Content', translate=True)