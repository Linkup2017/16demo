from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)



class AccountCardReceiptsImport(models.Model):
    _inherit = "account.card.receipts"

    def action_import(self):
        for sid in self :
            wiz = self.env['receipts.import.wizard'].create({
                'receipts_id': sid.id,
            })
            _logger.warning('---wiz %s', wiz.receipts_id)
            return {
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('account_card.receipts_import_wizard_form').id,
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'receipts.import.wizard',
                'res_id': wiz.id
            }
