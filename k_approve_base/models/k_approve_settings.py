# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettingsApproval(models.TransientModel):
    _inherit = 'res.config.settings'

    period = fields.Many2one('kapprove.retention', string="Default Retention Period", domain=[('permanent', '=', True)])
    is_sequential = fields.Boolean(string="Continue even if the parallel "
                                          "approver clicks REFUSE")

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsApproval, self).get_values()

        params = self.env['ir.config_parameter'].sudo()
        period = params.get_param('period', default=False)
        is_sequential = params.get_param('k_approve_base.is_sequential')

        res.update(
            period=int(period),
            is_sequential=is_sequential,
        )
        return res

    def set_values(self):
        super(ResConfigSettingsApproval, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("period", self.period.id)
        self.env['ir.config_parameter'].sudo().set_param(
            "k_approve_base.is_sequential",
            self.is_sequential)
