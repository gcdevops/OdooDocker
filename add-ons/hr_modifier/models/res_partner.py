from odoo import models, fields
import pytz

# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]
def _tz_get(self):
    return _tzs

class Partner(models.Model):
    _inherit = 'res.partner'
    tz = fields.Selection(_tz_get, string='Timezone', default='America/Montreal',
            help="When printing documents and exporting/importing data, time values are computed according to this timezone.\n"
                "If the timezone is not set, UTC (Coordinated Universal Time) is used.\n"
                "Anywhere else, time values are computed according to the time offset of your web client.")