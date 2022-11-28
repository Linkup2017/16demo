# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.exceptions import UserError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

import io
try:
	import xlrd
except ImportError:
	_logger.debug('Cannot `import xlrd`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')

class FmeaImportWizard(models.TransientModel):
    _name = 'receipts.import.wizard'
    _description = 'Card Receipts Import Wizard'

    receipts_id = fields.Many2one('account.card.receipts', string='Process', ondelete='set null')
    xls_file = fields.Binary('Excel File')
    account_card_id = fields.Many2one('account.card.no', string='card id')


    def action_import(self):

        try:
            book = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')

        for sheet in book.sheets():
            try:
                line_vals = []
                if sheet.name == 'Sheet1':
                    for row in range(sheet.nrows):
                        if row >= 1:
                            row_values = sheet.row_values(row)
                            row_data = row_values[4]
                            _logger.info('------------- row_values %s -----------', row_data)
                            new_data = row_data.replace('-', '')
                            _logger.info('------------- new_data %s -----------', new_data)
                            python_date = datetime(*xlrd.xldate_as_tuple(row_values[1], 0))
                            card_id = self.env['account.card.no'].search([])
                            for i in card_id:
                                _logger.info('------------- card_id %s -----------', i.backup_card_no)
                                if i.backup_card_no == new_data:
                                    data_id = i.id
                                    _logger.info('------------- data_id %s -----------', data_id)
                            self.env['account.card.receipts'].create({
                                'name': row_values[3],
                                'bank_code': row_values[3],
                                'card_no_code': data_id,
                                'card_type': row_values[0],
                                'card_no': row_values[4],
                                'store_id': row_values[2],
                                'approve_datetime': python_date,
                                'total': row_values[5],
                                'expense_state': 'waiting',
                                'approve_no': row_values[9],
                                'sply_amount': row_values[10],
                                'vat_amount': row_values[11],
                            })
            except IndexError:
                pass

    #
    # def action_import(self):
    #     wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
    #     for sheet in wb.sheets():
    #         for row in range(sheet.nrows):
    #             card_type = None
    #             approve_date = None
    #             store_name = None
    #             bank_name = None
    #             card_number = None
    #             total = None
    #             purpose = None
    #             remark = None
    #
    #             for col in range(sheet.ncols):
    #                 if sheet.cell(row, col).value:
    #                     if row > 3:
    #                         if col == 0:
    #                             card_type = sheet.cell(row, col).value
    #                         if col == 1:
    #                             approve_date = sheet.cell(row, col).value
    #                         if col == 2:
    #                             store_name = sheet.cell(row, col).value
    #                         if col == 3:
    #                             bank_name = sheet.cell(row, col).value
    #                         if col == 4:
    #                             card_number = sheet.cell(row, col).value
    #                         if col == 5:
    #                             total = sheet.cell(row, col).value
    #                         if col == 6:
    #                             purpose = sheet.cell(row, col).value
    #                         if col == 7:
    #                             remark = sheet.cell(row, col).value
    #
    #             if row > 3 :
    #                 if card_type :
    #                     x_obj = self.env['account.card.receipts'].create({
    #                         'name': bank_name,
    #                         'bank_code': bank_name,
    #                         'card_type': card_type,
    #                         'card_no': card_number,
    #                         'store_id': store_name,
    #                         'approve_datetime': approve_date,
    #                         'total': total,
    #                         'expense_state': 'waiting',
    #                         'purpose': purpose,
    #                         'remark': remark,
    #
    #                     })
    #                     _logger.info('------ name %s --------', card_type)

    # _inherit = 'account.journal'
    # _description = 'Card Receipts Import Wizard'
    # name = fields.Char(string='Journal Name')
    # receipts_id = fields.Many2one('account.card.receipts', string='Process', ondelete='set null')
    # xls_file = fields.Binary('Excel File')
    #
    # def action_import(self):
    #     wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
    #     for sheet in wb.sheets():
    #         for row in range(sheet.nrows):
    #             card_type = None
    #             approve_date = None
    #             store_name = None
    #             bank_name = None
    #             card_number = None
    #             total = None
    #             purpose = None
    #             remark = None
    #
    #             for col in range(sheet.ncols):
    #                 if sheet.cell(row, col).value:
    #                     if row > 3:
    #                         if col == 1:
    #                             card_type = sheet.cell(row, col).value
    #                         if col == 2:
    #                             approve_date = sheet.cell(row, col).value
    #                         elif col == 3:
    #                             store_name = sheet.cell(row, col).value
    #                         elif col == 4:
    #                             bank_name = sheet.cell(row, col).value
    #                         elif col == 5:
    #                             card_number = sheet.cell(row, col).value
    #                         elif col == 6:
    #                             total = sheet.cell(row, col).value
    #                         elif col == 7:
    #                             expense_state = sheet.cell(row, col).value
    #                         elif col == 8:
    #                             purpose = sheet.cell(row, col).value
    #                         elif col == 9:
    #                             remark = sheet.cell(row, col).value
    #
    #             if row > 3 :
    #                 if card_type :
    #                     x_obj = self.env['account.card.receipts'].create({
    #                         'name': bank_name,
    #                         'bank_code': bank_name,
    #                         'card_type': card_type,
    #                         'card_no': card_number,
    #                         'store_id': store_name,
    #                         'approve_datetime': approve_date,
    #                         'total': total,
    #                         'expense_state': 'approved',
    #                         'purpose': purpose,
    #                         'remark': remark,
    #
    #
    #                     })
    #                     _logger.info('------ name %s --------', card_type)
