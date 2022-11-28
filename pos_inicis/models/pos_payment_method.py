# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    def _get_payment_terminal_selection(self):
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [('inicis', 'Inicis')]

    inicis_tcode = fields.Selection(string="Inicis Transaction Code", selection=[
        ('card', 'Card'),
        ('unionpay', 'UnionPay'),
        ('cash_receipts', 'Cash receipts'),
        ('appcard', 'App Card'),
        ('lpay', 'L.Pay'),
        ('kakaopay', 'KakaoPay'),
        ('alipay', 'Alipay'),
        ('zeropay', 'ZeroPay'),
        ('bcqr', 'BC-UnionPay QR'),
        ('naverpay', 'NaverPay'),
    ], default='card')
    inicis_tid = fields.Char(string="Inicis Terminal ID", help='[Serial Number], for example: 8811000001',
                             copy=False)

    @api.onchange('inicis_tid')
    def _onchange_inicis_tid_warning(self):
        if self.use_payment_terminal == 'inicis':
            if len(self.inicis_tid or []) != 10:
                return {
                    'warning': {
                        'title': _("Warning"),
                        'message': _("Invalid Terminal serial number length.")
                    }
                }
