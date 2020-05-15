from odoo import fields, models 

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    administration_email = fields.Char(
        related="company_id.administration_email", readonly=False
    )