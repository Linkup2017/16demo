# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta


class RefuseApprovalWizard(models.TransientModel):
    _name = 'kapprove.refuse.wizard'
    _description = 'Refuse Approval'

    password = fields.Char(string="Password")
    comment = fields.Text(string="Comment", required=True)
    secret = fields.Boolean(string="Secret")

    def action_submit(self):
        if self.secret:
            self.env.user.sudo(self.env.user.id)._check_credentials(self.password, self.env)
        active_id = self.env.context.get('active_id')
        doc_id = self.env['kapprove.doc'].search([('id', '=', active_id)])
        params = self.env['ir.config_parameter'].sudo()
        is_sequential = params.get_param('k_approve_base.is_sequential')
        if self.comment:
            doc_id.message_post(
                body=_("%s Refused. %s") % (doc_id.name, self.comment))
        if doc_id.approver_ids:
            if doc_id.env.user.id in doc_id.approver_ids.mapped('user_id').ids:
                approver_id = doc_id.approver_ids.filtered(lambda l: l.user_id.id == doc_id.env.user.id)
                approver_id.write({
                    'state': 'refused',
                    'date': datetime.now()
                })
            # approve_status = doc_id.approver_ids.filtered(lambda l: l.state not in ['refused'])
                if is_sequential:
                    if approver_id.approve_type == 'parallel':
                        doc_id.write({
                            'state': 'in_progress'
                        })
                    else:
                        doc_id.write({
                            'state': 'refused'
                        })
                else:
                    doc_id.write({
                        'state': 'refused'
                    })
                doc_id._compute_approval_process_all()

