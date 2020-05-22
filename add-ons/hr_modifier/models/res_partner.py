from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Partner(models.Model):
    _inherit = 'res.partner'
    tz = fields.Selection(default='America/Montreal')
    x_partner_type = fields.Selection(
        [
            ('Backend - Programs','Backend - Programs'),
            ('Call Center','Call Center'),
            ('CPP/OAS Processing Centre','CPP/OAS Processing Centre'),
            ('EI & CPP/OAS Processing Centre','EI & CPP/OAS Processing Centre'),
            ('EI Call Centre','EI Call Centre'),
            ('EI Call Centre & Processing','EI Call Centre & Processing'),
            ('EI Processing','EI Processing'),
            ('EI Processing - Satellite','EI Processing - Satellite'),
            ('EI Processing & IPOC','EI Processing & IPOC'),
            ('EI Processing-IPOC-Call Centre','EI Processing-IPOC-Call Centre'),
            ('IPOC','IPOC'),
            ('NHQ','NHQ'),
            ('Other ESDC Office','Other ESDC Office'),
            ('Passport','Passport'),
            ('Processing Center','Processing Center'),
            ('RHQ','RHQ'),
            ('SCC (Service Canada Center)','SCC (Service Canada Center)'),
            ('SSC (Shared Services Canada)','SSC (Shared Services Canada)'),
            ('Warehouse','Warehouse')
        ],
        string = "Building Type"
    )
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
        street_regex = "[^a-zA-ZÀ-Öà-ö\s\-\d&.,':]"
        for record in self:
            if record.street:
                res = re.search(street_regex, record.street)
                if res:
                    raise ValidationError("The street field contains an invalid character: " + res.group(0))
            if record.street2:
                res = re.search(street_regex, record.street)
                if res:
                    raise ValidationError("The street 2 field contains an invalid character: " + res.group(0))

    # allow letters, spaces, and hyphens
    @api.constrains("city")
    def _check_city_allowed_characters(self):
        for record in self:
            if record.city:
                res = re.search("[^a-zA-ZÀ-Öà-ö\s\-\d&.,']", record.city)
                if res:
                    raise ValidationError("The city field contains an invalid character: " + res.group(0))

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
                res = re.search(phone_disallowed_chars, record.phone)
                if res:
                    raise ValidationError("The phone number contains an invalid character: "+ re.group(0))
            if record.mobile:
                res = re.search(phone_disallowed_chars, record.mobile)
                if res:
                    raise ValidationError("The mobile phone number contains an invalid character: " + res.group(0))

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