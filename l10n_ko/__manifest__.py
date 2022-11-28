# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'KOREA - Accounting',
    'version': '2.0',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
Chart of Accounts for Korea.
===============================

Thai accounting chart and localization.
    """,
    'author': 'Linkup Infotech',
    'website': 'http://link-up.co.kr/',
    'depends': ['account', 'base'],
    'data': [
        'data/account_data.xml',
        'data/l10n_ko_chart_data.xml',
        'data/account.account.template.csv',
        'data/l10n_ko_chart_post_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_chart_template_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'post_init_hook': '_preserve_tag_on_taxes',
    'license': 'LGPL-3',
}
