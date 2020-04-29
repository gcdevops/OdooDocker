from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Partner(models.Model):
    _inherit = 'res.partner'
    tz = fields.Selection(default='America/Montreal')

    # Validation

    # allow upper case, lower case, hyphens
    @api.constrains("name")
    def _check_name_allowed_characters(self):
        for record in self:
            if record.name:
                if not re.search("[a-zA-Z\s\- \.]", record.name):
                    raise ValidationError("The location name can only contain letters, spaces, and hyphens")

    # allow alphanumeric, spaces, and hyphens
    @api.constrains("street", "street2")
    def _check_street_allowed_characters(self):
        street_regex = "[a-zA-Z\s\-\d]"
        for record in self:
            if record.street:
                if not re.search(street_regex, record.street):
                    raise ValidationError("The street field can only contain letters, numbers, and hyphens")
            if record.street2:
                if not re.search(street_regex, record.street2):
                    raise ValidationError("The street 2 field can only contain letters, numbers, hyphens")
    
    # allow letters, spaces, and hyphens
    @api.constrains("city")
    def _check_city_allowed_characters(self):
        for record in self:
            if record.city:
                if not re.search("[a-zA-Z\s\-]", record.city):
                    raise ValidationError("The city field can only contain letters")
    
    # allow postal code formats, uppercase or lowercase, space or no space
    @api.constrains("zip")
    def _check_postal_code_allowed_characters(self):
        for record in self:
            if record.zip:
                if not re.search("^([a-zA-Z]\d[a-zA-Z][ ]?\d[a-zA-Z]\d)$", record.zip):
                    raise ValidationError("The postal code is invalid")
    
    @api.constrains("phone", "mobile")
    def _check_phone_allowed_characters(self):
        for record in self:
            phone_disallowed_chars = "[^\d\-]"
            if record.phone:
                if re.search(phone_disallowed_chars, record.phone):
                    raise ValidationError("The phone number can only contain numbers, hyphens")
            if record.mobile:
                if re.search(phone_disallowed_chars, record.mobile):
                    raise ValidationError("The mobile phone number can only contain numbers, hyphens")

    # if special characters are found, raise an error
    @api.constrains("email")
    def _check_email_allowed_characters(self):
        for record in self:
            if record.email:
                res = re.search(r"['\"*?;/\\]", record.email)
                if res:
                    raise ValidationError("The email contains an invalid character: " + res.group(0))

    # if special characters are found, raise an error
    @api.constrains("website")
    def _check_website_allowed_characters(self):
        for record in self:
            if record.website:
                res = re.search(r"[^\w\d\-.~:/?#\[\]@!$&'()*+,;=]", record.website)
                if res:
                    raise ValidationError("The website url contains an invalid character: " + res.group(0))