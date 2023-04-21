from datetime import datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class RequestLegalServices(models.Model):
    _name = 'request.legal.services'
    _description = 'Request Legal Services'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True, copy=False, default='New', tracking=True)
    nature_of_request = fields.Selection(selection=[('contract', 'Contract'),
                                                    ('dedication', 'Dedication'),
                                                    ('deed', 'Deed'),
                                                    ('easement', 'Easement'),
                                                    ('legal_opinion', 'Legal Opinion'),
                                                    ('ordinance', 'Ordinance'),
                                                    ('other', 'Other'),
                                                    ('resolution', 'Resolution'),
                                                    ('subpoena', 'Subpoena'),
                                                    ('vacation_of_r-o-w', 'Vacation of R-O-W')],
                                         string='Nature of Request', tracking=True)
    assigned_attorney_id = fields.Many2one('res.users', string='Attorney Assigned', domain="[(1, '=', 1)]", tracking=True)
    active = fields.Boolean(default=True)
    note = fields.Text(string="Description", widget='html', required=True)
    description = fields.Text(string="Description")
    start_datetime = fields.Datetime(string="Start Date", default=fields.Datetime.now)
    due_date = fields.Date(string='Due Date', required=True, tracking=True, default=lambda self: fields.Date.today() + relativedelta(days=9))
    days_remaining = fields.Integer(string='Days Remaining', compute='_compute_days_remaining')


    state = fields.Selection([
        ('new', 'New'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string='Status', default='new')

    @api.depends('due_date')
    def _compute_days_remaining(self):
        for record in self:
            if record.due_date:
                due_date = fields.Date.from_string(record.due_date)
                today_date = fields.Date.from_string(fields.Date.today())
                remaining_days = (due_date - today_date).days
                record.days_remaining = remaining_days + 1

    @api.depends('state')
    def _compute_is_open(self):
        for record in self:
            record.is_open = record.state == "open"  # Replace "your_status_field" with the field used to track the status of the RLS record
    @api.onchange('nature_of_request')
    def _onchange_nature_of_request(self):
        if self.nature_of_request == 'contract':
            self.due_date = fields.Date.to_string(fields.Date.today() + relativedelta(days=29))
        else:
            self.due_date = fields.Date.to_string(fields.Date.today() + relativedelta(days=9))

    def create_request(self):
        vals = {
            'name': self.name,
            'nature_of_request': self.nature_of_request,
            'assigned_attorney_id': self.assigned_attorney_id.id,
            'note': self.note,
            'start_datetime': datetime.now(),
            'due_date': self.due_date,
        }
        return self.env['request.legal.services'].create(vals)

class UpdateDaysRemaining(models.Model):
    _name = 'update.days.remaining'
    _description = 'Update Days Remaining'

    def _update_days_remaining(self):
        requests = self.env['request.legal.services'].search([])
        requests._compute_days_remaining()

    @api.model
    def _schedule_cron(self):
        # Check if the scheduled action already exists
        cron_exist = self.env.ref('request.legal.services.update_days_remaining_cron', False)
        if cron_exist:
            return

        # Create the scheduled action
        self.env['ir.cron'].create({
            'name': 'Update Days Remaining',
            'user_id': self.env.ref('base.user_admin').id,
            'interval_number': 1,
            'interval_type': 'days',
            'numbercall': -1,
            'doall': False,
            'model_id': self.env.ref('request.legal.services.model_update_days_remaining').id,
            'function': '_update_days_remaining',
            'args': '()',
            'nextcall': fields.Datetime.to_string(fields.Datetime.combine(fields.Date.today(), time(0, 5, 0))),
            'priority': 1,
            'active': True,
            'code': 'model._update_days_remaining()'
        })


class RequestLegalServicesDashboard(models.Model):
    _name = 'request.legal.services.dashboard'
    _description = 'Request Legal Services Dashboard'
    _auto = False

    total_requests = fields.Integer(string="Total Requests", compute='_compute_request_counts')
    open_requests = fields.Integer(string="Open Requests", compute='_compute_request_counts')
    weekly_requests = fields.Integer(string="Weekly Requests", compute='_compute_request_counts')

    def _compute_request_counts(self):
        request_env = self.env['request.legal.services']
        for record in self:
            record.total_requests = request_env.search_count([('active', '=', True)])
            record.open_requests = request_env.search_count([('state', '=', 'open')])

            today = fields.Date.today()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)

            record.weekly_requests = request_env.search_count([
                ('create_date', '>=', week_start),
                ('create_date', '<=', week_end)
            ])
