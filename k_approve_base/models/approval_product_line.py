# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class kApprovalProductLine(models.Model):
    _name = 'kapproval.product.line'
    _description = 'Product Line'

    _check_company_auto = True

    approval_request_id = fields.Many2one('kapprove.doc', required=True)
    description = fields.Char("Description")
    company_id = fields.Many2one(
        string='Company', related='approval_request_id.company_id',
        store=True, readonly=True, index=True)
    product_id = fields.Many2one('product.product', string="Products", check_company=True)
    product_uom_id = fields.Many2one('uom.uom', string="Unit of Measure",
        domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    quantity = fields.Float("Quantity", default=1.0)
    amount = fields.Float('Amount',  digits='Product Price', default=0.0)

    str_has_product = fields.Char(string="has_product", related="approval_request_id.str_has_product")
    str_has_quantity = fields.Char(string="has_quantity", related="approval_request_id.str_has_quantity")
    str_has_amount = fields.Char(string="has_amount", related="approval_request_id.str_has_amount")
    str_has_reference = fields.Char(string="has_reference", related="approval_request_id.str_has_reference")


    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id
            if not self.description:
                self.description = self.product_id.display_name
        else:
            self.product_uom_id = None
