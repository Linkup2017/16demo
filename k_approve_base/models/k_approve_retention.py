# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KApproveRetention(models.Model):
    _name = 'kapprove.retention'
    _inherit = ['mail.thread']
    _description = "Retention Period"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    period = fields.Integer('Retention Period', default=0)
    permanent = fields.Boolean(string="Active", default=False)
    date_period = fields.Selection([
        ('days', 'Days'),
        ('months', 'Months'),
        ('years', 'Years'),
    ], string='Date Period', default='days', required=True)

    @api.onchange('period', 'date_period')
    def _onchange_period(self):
        """
                Onchange function for calculating the retention name based on the period and date period selected.
                """
        self.name = str(self.period) + ' ' + self.date_period
