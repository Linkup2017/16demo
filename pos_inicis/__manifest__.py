# -*- coding: utf-8 -*-
{
    'name': 'POS Inicis',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Integrate your POS with an Inicis payment terminal',
    'description': '',
    'data': [
        'views/pos_payment_method_views.xml',
        'views/res_config_setting_views.xml',
    ],
    'depends': ['point_of_sale'],
    'installable': True,
    'assets': {
        'point_of_sale.assets': [
            'pos_inicis/static/**/*',
        ],
        'web.assets_qweb': [
            'pos_inicis/static/src/xml/**/*',
        ],
    },
    'license': 'LGPL-3',
}
