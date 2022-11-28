# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class AccountCardNumberList(models.Model):
    _name = 'account.card.no'

    name = fields.Char(string='Card Name', required=True)
    card_code = fields.Char(string='Card Code')
    _sql_constraints = [
        ('name_unique', 'unique(name, backup_card_no)', "Card Number must be unique.")
    ]


