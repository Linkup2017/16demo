# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: Inicis',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 350,
    'summary': "A payment provider for running fake payment flows for inicis purposes.",
    'depends': ['payment'],
    'data': [
        'views/payment_inicis_templates.xml',
        'views/payment_views.xml',
        'views/payment_transaction_views.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_inicis/static/src/js/**/*',
            'payment_inicis/static/src/css/**/*',
        ],
    },
    'license': 'LGPL-3',
}
