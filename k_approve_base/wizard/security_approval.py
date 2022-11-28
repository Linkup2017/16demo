# -*- coding: utf-8 -*-

from odoo import models, fields, _
from datetime import datetime, timedelta


class SecurityApprovalWizard(models.TransientModel):
    _name = 'kapprove.security.wizard'
    _description = 'Security Approval'

    password = fields.Char(string="Password", required=True)
    comment = fields.Text(string="Comment")

    def action_submit(self):
        self.env.user.sudo(self.env.user.id)._check_credentials(self.password, self.env)
        active_id = self.env.context.get('active_id')
        doc_id = self.env['kapprove.doc'].search([('id', '=', active_id)])
        if self.comment:
            doc_id.message_post(
                    body=_("%s") % (self.comment))
        if doc_id.approver_ids:
            if doc_id.env.user.id in doc_id.approver_ids.mapped('user_id').ids:
                approver_id = doc_id.approver_ids.filtered(lambda l: l.user_id.id == doc_id.env.user.id)
                approver_id.write({
                    'state': 'approved',
                    'date': datetime.now()
                })
            approve_status = doc_id.approver_ids.filtered(lambda l:l.state not in ['approved'])
            last_approver = self.env['kapprove.doc.template.flow'].search([('id', '=', max(doc_id.approver_ids.ids))])
            if last_approver.state == 'approved':
                doc_id.write({
                    'state': 'approved',
                    'approve_date': datetime.now().date()
                })

            else:
                doc_id.write({
                    'state': 'in_progress'
                })

