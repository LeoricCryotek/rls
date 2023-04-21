from odoo import http


class RlSDashboardController(http.Controller):

    @http.route('/rls/data', type='json', auth='user')
    def rls_dashboard_data(self):
        # Fetch the data required for the dashboard

        # Example data format (you need to replace this with the actual data from your models)
        data = {
            'open_requests': [
                {'attorney_name': 'Attorney 1', 'open_requests': 5},
                {'attorney_name': 'Attorney 2', 'open_requests': 7},
            ],
            'weekly_requests': [
                {'day': 'Monday', 'new_requests': 2},
                {'day': 'Tuesday', 'new_requests': 1},
                {'day': 'Wednesday', 'new_requests': 0},
                {'day': 'Thursday', 'new_requests': 3},
                {'day': 'Friday', 'new_requests': 4},
            ],
        }

        return data
