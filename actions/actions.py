from odoo import api, models, fields
from datetime import datetime, timedelta


class RequestLegalServicesActions(models.Model):
    _inherit = 'request.legal.services'

    @api.depends('start_datetime', 'due_date')
    def _compute_weekly_requests(self):
        for record in self:
            if record.start_datetime and record.due_date:
                start_datetime = fields.Date.from_string(record.start_datetime)
                due_date = fields.Date.from_string(record.due_date)
                date_diff = (due_date - start_datetime).days + 1
                weeks = (date_diff + start_datetime.weekday()) // 7

                if (date_diff % 7 + start_datetime.weekday()) % 7:
                    weeks += 1

                record.weekly_requests = weeks
            else:
                record.weekly_requests = 0
