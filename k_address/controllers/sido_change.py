# -*- coding: utf-8 -*-


from odoo import fields, http, _
from odoo.exceptions import AccessError, AccessDenied, MissingError
from odoo.http import request

import logging

_logger = logging.getLogger(__name__)

class Sido_change(http.Controller):
    @http.route('/web/view/edit_sido_address',type='json', auth="user")
    def edit_sido_address(self, sido,lang):
        _logger.warning("--sido-- %s lang %s", sido,lang)

        return request.env['res.partner'].sudo()._set_korea_address(sido,lang)
