# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)
import json

class KApproveDocLineUser(models.Model):
    _name = 'kapprove.doc.line'
    _description = "Approval Document Line"

    approve_doc_id = fields.Many2one('kapprove.doc',string = 'Approve',ondelete='cascade',index=True )
    name = fields.Char(string="Name", related='approve_doc_id.name')
    doc_name = fields.Char(string="Document Title",related='approve_doc_id.doc_name')
    approver_id = fields.Many2one('res.users', string="Approver")
    user_id = fields.Many2one('res.users' , string="Created By",related='approve_doc_id.user_id')
    create_on = fields.Datetime(string="Creation On")
    tag_ids = fields.Many2many('kapprove.doc.tag', string="Tags",related='approve_doc_id.tag_ids')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('in_progress', 'In progress'),
        ('approved', 'Approved'),
        ('refused', "Refused"),
        ('cancel', 'Cancel')
    ], 'State', related='approve_doc_id.state')


    approval_state = fields.Selection([('to_approval', 'To approval'), ('approved', 'Approved')],
                                      string='Approval State')
    checked_state = fields.Selection([('to_checked', 'To checked'), ('checked', 'Checked')],
                                     string='Checked State')
    mine_state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('in_progress', 'In progress'),
        ('approved', 'Approved'),
        ('refused', "Refused"),
        ('cancel', 'Cancel')
    ], 'My document')


    # def set_panel_select_range(self):
    #     _logger.warning('--**set_panel_select_range')
    #     scat = {'category_domain': [['approval_state', '=', 'to_approval']], 'enable_counters': True, 'expand': True,
    #      'filter_domain': [], 'hierarchize': True, 'limit': 200,
    #      'search_domain': ['&', ['approver_id', '=', 2], '|', ['approval_state', '!=', False], '|',
    #                        ['checked_state', '!=', False], ['mine_state', '!=', False]]}
    #
    #     self.search_panel_select_range('approval_state')
    #     self.search_panel_select_range('checked_state')
    #     self.search_panel_select_range('mine_state')
