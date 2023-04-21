{
    'name': 'Request for Legal Services',
    'version': '1.2',
    'author': 'Danny Santiago',
    'category': 'Services/Legal',
    'website':'https://home.cityoflewiston.org',
    'sequence': 15,
    'license': 'LGPL-3',
    'summary': 'Track request for legal services and their status. ',
    'description': "The best tool around for Legal Service Requests",
    'depends': [
        'base',
        'mail',
        'calendar',
        'web',
        'crm',
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/menu.xml',
        'views/rls_dashboard_view.xml',
        'views/request_legal_services.xml',
        'views/rls_templates.xml',
        'views/ir_cron_data.xml',
        'actions/actions.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
    'qweb': [
    ],
    'demo': [
    ],
    'js': [
        'static/src/js/gauge_field.js',
    ],
    'css': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
