# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('inicis', 'Inicis')], ondelete={'inicis': 'set default'})
    inicis_mid = fields.Char(string="Merchant ID", required_if_provider='inicis')
    inicis_mid_key = fields.Char(string="Merchant ID Key", required_if_provider='inicis')
    inicis_sign_key = fields.Char(string="Sign Key", required_if_provider='inicis')

    # === COMPUTE METHODS ==
    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'inicis').update({
            'support_fees': True,
            'support_manual_capture': True,
            'support_refund': 'partial',
            'support_tokenization': True,
        })

