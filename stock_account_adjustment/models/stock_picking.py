# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _adjust_stock_accounting(self):
        svl_vals_list = []
        stock_moves = self.move_lines.filtered(lambda move: move.state == 'done')
        for stock_move in stock_moves:
            value = sum(stock_move.stock_valuation_layer_ids.mapped('value'))
            account_move_line = self.env['account.move.line'].search(
                [('purchase_line_id', '=', stock_move.purchase_line_id.id)])

            if account_move_line and account_move_line.move_id.state == 'posted' and account_move_line.balance != value:
                diff = account_move_line.balance - value
                svl_vals = {
                    'value': diff,
                    'unit_cost': 0,
                    'quantity': 0,
                    'remaining_qty': 0,
                    'stock_valuation_layer_id': stock_move.stock_valuation_layer_ids.ids[0],
                    'description': account_move_line.move_name and '%s - %s' % (account_move_line.move_name, stock_move.product_id.name) or stock_move.product_id.name,
                    'stock_move_id': stock_move.id,
                    'product_id': stock_move.product_id.id,
                    'company_id': stock_move.company_id.id,
                }
                svl_vals_list.append(svl_vals)
        return self.env['stock.valuation.layer'].sudo().create(svl_vals_list)

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self._adjust_stock_accounting()
        return res