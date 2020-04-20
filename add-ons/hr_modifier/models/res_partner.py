from odoo import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'
    tz = fields.Selection(default='America/Montreal')