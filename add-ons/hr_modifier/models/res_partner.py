from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Partner(models.Model):
    _inherit = 'res.partner'
    tz = fields.Selection(default='America/Montreal')


    # Validation

    @api.constrains("street", "street2")
    def _check_street_allowed_character(self):
        for record in self:
            if record.street:
                if re.search("[^a-zA-Z\s\-\d]", record.street):
                    raise ValidationError("The street field can only contain letters, numbers, and hyphens")
            if record.street2:
                if re.search("[^a-zA-Z\s\-\d#]", record.street2):
                    raise ValidationError("The street 2 field can only contain letters, numbers, hyphens, and #")