from odoo import models, fields, api, _
from odoo.addons.base.models.res_partner import WARNING_HELP, WARNING_MESSAGE
from odoo.exceptions import ValidationError, UserError
import xlwt, xlsxwriter, xlrd
import base64
import logging
from operator import itemgetter
import datetime

_logger = logging.getLogger(__name__)


class Fmeaprocess(models.Model):
    _inherit = "account.card.receipts"

    def action_import(self):
        for sid in self :
            wiz = self.env['receipts.import.wizard'].create({
                'receipts_id': sid.id,
            })
            _logger.warning('---wiz %s', wiz.receipts_id)
            return {
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('account_card_receipts.receipts_import_wizard_form').id,
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'receipts.import.wizard',
                'res_id': wiz.id
            }