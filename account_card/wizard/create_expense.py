from odoo import _, api, exceptions, fields, models
from popbill import EasyFinBankService, PopbillException, ContactInfo, JoinForm, CorpInfo, BankAccountInfo
from datetime import datetime, timedelta
import json
import requests
from urllib import parse
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)



class CreateExpenseReport(models.TransientModel):
    _name = 'create.expense.wizard'

    def _default_session(self):
        return self.env['account.card.receipts'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('account.card.receipts', 'store_id', 'total', 'product_id', string='Line', default=_default_session)

    def create_expense(self):

        expense_id = self.env['hr.expense'].search([])
        create = 0
        expense_list = []
        for value in expense_id:
            expense_list.append(value.seq_id)
            _logger.info('---------- value %s ---------', expense_list)
        for li in self.session_ids:
            _logger.info('-------------- state %s ---------', li.approve_no)
            if li:
                if li.remark:
                    remark = str(li.remark)
                else:
                    remark = ''

                if li.purpose:
                    purpose = str(li.purpose)
                else:
                    purpose = ''

                if li.expense_state == 'waiting':
                    if li.approve_no not in expense_list:
                        value = self.env['hr.expense'].create({
                            "name": li.store_id,
                            "product_id": li.product_id.id,
                            "unit_amount": li.total,
                            "employee_id": li.employee_id.id,
                            "description": purpose + "\n" + remark,
                            "seq_id": li.approve_no,
                        })

                    li.expense_state = 'exported'
                    _logger.info('-------------- state %s ---------', li.approve_no)
                    _logger.info('-------------- expense_list %s ---------', expense_list)
                    _logger.info('--------------- 생성 ----------')
                    create += 1
                    _logger.info('--------------- create %s ------------', create)
                else:
                    raise UserError('You can create report "Unreported lines" only.')

            else:
                _logger.info('----------------- 미생성 ----------------')
        # if create > 0:
        #     return {
        #         'name': _('Connected'),
        #         'type': 'ir.actions.act_window',
        #         'view_mode': 'form',
        #         'res_model': 'expense.check',
        #         'target': 'new',
        #     }

