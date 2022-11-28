# -*- coding: utf-8 -*-

{
    'name': 'Account Card',
    'version': '15',
    "summary": "Account Card",
    "author": "LinkUp Info Tech",
    "license": "OPL-1",
    'depends': ['base', 'account', 'hr', 'mail', 'hr_expense', "kr_pb_bank"],
    'assets': {
        'web.assets_backend': [
            'account_card/static/src/js/list_controller.js',
        ],
    },

    'data': [

        'wizard/create_expense_form.xml',
        'wizard/import_excel.xml',
        'views/card_receipts_view.xml',
        'views/config_views.xml',
        'views/card_list_view.xml',
        'views/card_list_no_view.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'wizard/message_form.xml',
        'wizard/message_expense_form.xml',
        "data/ir_cron.xml",
    ],
}
