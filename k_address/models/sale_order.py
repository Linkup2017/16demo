# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, models, fields
from odoo.tools.translate import _


import logging
#Get the logger
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    image_id = fields.Image("Logo", max_width=128, max_height=128)