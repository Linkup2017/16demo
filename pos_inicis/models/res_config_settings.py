# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_pos_inicis = fields.Boolean(string="Inicis Payment Terminal", help="The transactions are processed by Inicis. Set your Inicis credentials on the related payment method.")
