# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class KApproverLine(models.Model):
    _name = 'kapprove.line'
    _inherit = ['mail.thread']
    _description = "My Approver Line"
    _rec_name = 'name'

    name = fields.Text(string="Name", required=True)
    approver_ids = fields.One2many(comodel_name='kapprove.flow.line', inverse_name='rel_line_approver_ids', string="Approvers")
    cooperation_user_ids = fields.Many2many('res.users', 'rel_approve_line', string="Cooperation")
    users = fields.Many2many('res.users', compute='_compute_users')

    @api.model
    def _default_user(self):
        """
            Function for fetching the default user
        """
        return self.env.context.get('user_id', self.env.user.id)

    user_id = fields.Many2one('res.users', readonly=True, string="Created By", required=True, default=_default_user)

    @api.depends('approver_ids')
    def _compute_users(self):
        if self.approver_ids:
            user_id = self._default_user()
            users_ids = self.approver_ids.mapped('user_id')
            filtered_user_ids = users_ids.filtered(lambda l: l.id != user_id)

            self.users += filtered_user_ids
        else:
            self.users = None

