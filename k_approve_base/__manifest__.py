# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Technologies (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

{
    'name': 'K Approvals base',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Korea Approval""",
    'description': "Korea Approval",
    'author': 'Linkup Info Tech',
    'website': "http://www.link-up.co.kr",
    'company': 'Linkup Info Tech',
    'maintainer': 'Linkup Info Tech',
    'depends': ['base', 'product','hr','web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/kapprove_view.xml',
        'views/kapprove_categ_view.xml',
        'views/kapprove_tag_view.xml',
        'views/k_approve_retention_view.xml',
        'views/kapprove_template_view.xml',
        'views/k_approve_settings_view.xml',
        'views/kapprove_doc_view.xml',
        'views/kapprove_doc_line_view.xml',
        'views/kapprove_doc_share_view.xml',
        'views/kapprove_received_approval_view.xml',
        'views/hr_signature.xml',
        'wizard/template_wizard.xml',
        'wizard/security_approval.xml',
        'wizard/refuse_approve_wizard.xml',
        'reports/k_approve_report.xml',
        'views/report_template.xml',
        'views/kapprove_doc_approver_line.xml',
        'views/approval_product_line_views.xml',
        'wizard/approval_wizard.xml',
            ],
    'assets': {
   
        'web.assets_backend': [
            '/k_approve_base/static/src/js/searchpanel.js',
            # '/k_approve_base/static/src/js/activity.js',
            '/k_approve_base/static/src/form/form_renderer.js',
            '/k_approve_base/static/src/list/list_renderer.js',
            '/k_approve_base/static/src/list/list_renderer_ext.js',
            '/k_approve_base/static/src/scss/style_backend.scss',
            '/k_approve_base/static/src/scss/style.scss',
            '/k_approve_base/static/src/xml/web_kanban_activity.xml',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
