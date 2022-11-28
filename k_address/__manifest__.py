
{
    'name': 'Korea address',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Korea Address""",
    'description': "Korea Address",
    'author': 'Linkup info tech',
    'website': "https://www.link-up.co.kr",
    'company': 'Linkup info tech',
    'maintainer': 'Linkup info tech Solutions',
    'depends': ['contacts','sale_management'],
    'assets': {
        'web.assets_backend': [
            '/k_address/static/src/js/postcode.v2.js',
            '/k_address/static/src/js/form_view.js',
            '/k_address/static/src/js/render_view.js',
            '/k_address/static/src/js/control_view.js',
            '/k_address/static/src/js/relational_fields.js',
        ],
    },
    'data': [
        'views/kaddress_view.xml',
        'views/sale_order.xml',
        'data/address.xml',
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
