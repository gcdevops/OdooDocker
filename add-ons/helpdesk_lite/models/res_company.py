from odoo import api, models, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    administration_email = fields.Char(
        'Administration Email',
        default="you@example.com",
        help="email of the admin of which to send ticket updates",
    )

    