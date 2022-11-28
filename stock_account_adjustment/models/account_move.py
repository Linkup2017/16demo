# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _adjust_stock_accounting(self):
        svl_vals_list = []
        for line in self.line_ids:
            stock_move = self.env['stock.move'].search(
                [('purchase_line_id', '=', line.purchase_line_id.id),
                 ('state', '=', 'done')])
            if stock_move:
                value = sum(stock_move.stock_valuation_layer_ids.mapped('value'))
                if line.balance != value:
                    diff = line.balance - value
                    svl_vals = {
                        'value': diff,
                        'unit_cost': 0,
                        'quantity': 0,
                        'remaining_qty': 0,
                        'stock_valuation_layer_id': stock_move.stock_valuation_layer_ids.ids[0],
                        'description': line.move_name and '%s - %s' % (
                            line.move_name, stock_move.product_id.name) or stock_move.product_id.name,
                        'stock_move_id': stock_move.id,
                        'product_id': stock_move.product_id.id,
                        'company_id': stock_move.company_id.id,
                    }
                    svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)

    def _post(self, soft=True):
        posted = super()._post(soft)

        self._adjust_stock_accounting()
        return posted