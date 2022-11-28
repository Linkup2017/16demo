# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    kaddress_bool = fields.Boolean("Use Korea Address?")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        kaddress_bool = ICPSudo.get_param('k_address.kaddress_bool')
        res.update(
            kaddress_bool=kaddress_bool,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param("k_address.kaddress_bool", self.kaddress_bool or '')



