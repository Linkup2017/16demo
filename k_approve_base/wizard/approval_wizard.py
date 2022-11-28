# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta


class ApprovalWizard(models.TransientModel):
    _name = 'approval.wizard'
    _description = 'Approval Wizard'

    comment = fields.Text(string="Comment")

    def done(self):
        active_id = self.env.context.get('active_id')
        doc_id = self.env['kapprove.doc'].search([('id', '=', active_id)])
        if self.comment:
            doc_id.message_post(
                body=_("%s") % (self.comment))


class ApproverSelectWizard(models.TransientModel):
    _name = 'approver.select.wizard'

    message = fields.Text('Message', required=True)

    def done(self):
        _logger.warning('Submitted Document without Approvers')
        active_id = self.env.context.get('active_id')
        doc_id = self.env['kapprove.doc'].search([('id', '=', active_id)])
        doc_id.write({
            'state': 'approved',
            'approve_date': datetime.now().date()
        })

