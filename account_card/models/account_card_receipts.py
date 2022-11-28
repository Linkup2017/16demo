# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
import json
import requests
from urllib import parse
from datetime import datetime, timedelta
from odoo.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)

class AccountCardReceipts(models.Model):
    _name = 'account.card.receipts'
    _inherit = ["mail.thread"]


    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id

    @api.model
    def _get_product(self):

        set_product_id = self.env['ir.config_parameter'].sudo().get_param('account_card.product_id')
        if set_product_id:
            product_id = set_product_id
            return product_id

    def unlink(self):
        for card in self:
            card_id = self.env['hr.expense'].search([('seq_id', '=', card.approve_no)])
            _logger.info('----------- unlink %s --------', card_id)
            _logger.info('----------- unlink %s --------', card.approve_no)
            if card.approve_no == card_id.seq_id:
                raise UserError(_('경비에 생성되어 있는 내용은 삭제할 수 없습니다.'))
                #
                # for line in card_id:
                #     line.expense_state = 'waiting'
                #     _logger.info('------------ %s store_id -------------', line.store_id)
                #     _logger.info('------------ %s total -------------', line.total)
                #     _logger.info('------------ %s  -------------', line)

        super(AccountCardReceipts, self).unlink()



    name = fields.Char(string='New')
    date = fields.Date(string='Date', required=True, index=True, copy=False, default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', string='Company Name', default=lambda self: self.env.company)
    # bank_code = fields.Char('account.card.no', string='Bank name', required=True)
    bank_code = fields.Char(string='Bank name', required=True)
    card_no_code = fields.Char(string='Card Number')
    card_no = fields.Char(string='Card number', required=True)
    store_id = fields.Char(string='Store name', required=True)
    approve_datetime = fields.Datetime(string='Approve date', required=True)
    approve_no = fields.Char(string='Approve number', required=True)
    card_type = fields.Char(string='Card type', required=True)
    approve_can = fields.Selection([('approved', '정상'),
                                    ('canceled', '취소'),
                                    ], readonly=True)
    cancel_date = fields.Datetime(string='Cancel date')
    store_repre_name = fields.Char(string='Store representative name')
    store_tele_number = fields.Char(string='Store telephone number')
    store_address = fields.Char(string='Store address')
    foreign_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    total = fields.Monetary(currency_field='foreign_currency_id', string='Total', required=True)
    sply_amount = fields.Monetary(currency_field='foreign_currency_id', string='Supply amount', required=True)
    vat_amount = fields.Monetary(currency_field='foreign_currency_id', string='Vat', required=True)
    purpose = fields.Char(string='Purpose', default='')
    remark = fields.Char(string='Remark', default='')
    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee_id)
    expense_state = fields.Selection([('waiting', 'Not yet'),
                                   ('exported', 'Reported')],
                                  string='Expense state', readonly=True, default='waiting')
    # product_id = fields.Many2one('product.product', string='Product', default=lambda self: self.env.company.product_id)
    product_id = fields.Many2one('product.product', string='Product', default=_get_product)
    note = fields.Text(string='Description')
    seq = fields.Char(string='seq')


    def name_get(self):
        card_name_list = []
        for card in self:
            name = card.name
            if card.card_no:
                name = " {}".format(card.store_id)
            card_name_list.append((card.id, name))
        return card_name_list

    def onchange_cancel_date(self):
        _logger.info(' -- cancel date 작성 --')


    def action_import_receipt_item(self):

        items = self.env["account.card"].search([("card_no", '!=', None)])

        return self.action_import_receipt(items)

    def action_import_receipt(self, items):



        item = self.env['res.company'].search([('connect_card', '=', True)])
        list_id = self.env['account.card.receipts'].search([])
        _logger.info('-------------- item %s ------------', item.org_code)
        _logger.info('-------------- item %s ------------', item.biz_no)
        _logger.info('-------------- list_id %s ------------', list_id)
        api_list = []
        approve_no_list = []

        for li in list_id:
            approve_no_list.append(li.approve_no)
            _logger.info('-------------- li %s ------------', approve_no_list)

        for env in items:
            item = self.env['res.company'].search([('id', '=', env.company_id.id)])

            if item == None:
                return



        for i in items:
            # _logger.info('--------- %s i --------', value)
            API_HOST = "http://webankapi-dev.appplay.co.kr/gateway.do?JSONData="
            method = 'POST'
            headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}
            json_string = {
                "API_ID": "0410",
                "API_KEY": item.api_key,
                "ORG_CD": item.org_code,
                "REQ_DATA": {
                    "BIZ_NO": item.biz_no,
                    "CARD_NO": "",
                    "START_DATE": "20161101",
                    "START_TIME": "",
                    "END_DATE": "20161130",
                    "END_TIME": "",
                    "REQ_CNT": "",
                    "APV_CAN_YN": "",
                    "NEXT_KEY": ""
                }
            }
            json_Dict = json.dumps(json_string, ensure_ascii=False)
            JSONData = parse.quote_plus(str(json_Dict))
            url = API_HOST + JSONData

            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers)
            _logger.info("response status %r" % response.status_code)


            eval_response = response.text
            _logger.info("eval_response %r" % eval_response)
            to_json = json.loads(eval_response)

            for li in to_json['RES_DATA']:
                api_list.append(li['APV_NO'])


            for val in to_json['RES_DATA']:
                if not val:
                    _logger.info('-- ? --')
                    list_id.card_state = 'termination'

                if val['LST_MOD_DT']:
                    date = val['LST_MOD_DT']
                    write_date = datetime.strptime(date, '%Y%m%d%H%M%S')
                    _logger.info('------------- %s -----------', val['LST_MOD_DT'])

                if val['APV_NO'] not in str(approve_no_list):
                    _logger.info('---------------- %s val --------------', val)


                    '''
    
                     카드사 코드번호에 맞게 카드사 이름 변경
    
                    '''

                    if val['BANK_CD'] == '30000001':
                        bank_code = 'KB'
                    if val['BANK_CD'] == '30000002':
                        bank_code = '현대'
                    if val['BANK_CD'] == '30000003':
                        bank_code = '삼성'
                    if val['BANK_CD'] == '30000004':
                        bank_code = '외환'
                    if val['BANK_CD'] == '30000006':
                        bank_code = '비씨'
                    if val['BANK_CD'] == '30000008':
                        bank_code = '신한'
                    if val['BANK_CD'] == '30000010':
                        bank_code = '하나'
                    if val['BANK_CD'] == '30000012':
                        bank_code = '광주'
                    if val['BANK_CD'] == '30000013':
                        bank_code = '수협'
                    if val['BANK_CD'] == '30000014':
                        bank_code = '전북'
                    if val['BANK_CD'] == '30000015':
                        bank_code = '하나'
                    if val['BANK_CD'] == '30000016':
                        bank_code = '씨티'
                    if val['BANK_CD'] == '30000017':
                        bank_code = '아맥스(롯데)'
                    if val['BANK_CD'] == '30000018':
                        bank_code = '우리'
                    if val['BANK_CD'] == '30000019':
                        bank_code = '롯데(개인카드)'
                    if val['BANK_CD'] == '30000020':
                        bank_code = '산은'
                    if val['BANK_CD'] == '30000021':
                        bank_code = 'NH'
                    if val['BANK_CD'] == '30000060':
                        bank_code = '비씨(기업)'
                    if val['BANK_CD'] == '30000061':
                        bank_code = '비씨(SC)'
                    if val['BANK_CD'] == '30000062':
                        bank_code = '비씨(부산)'
                    if val['BANK_CD'] == '30000063':
                        bank_code = '비씨(대구)'
                    if val['BANK_CD'] == '30000064':
                        bank_code = '비씨(경남)'
                    if val['BANK_CD'] == '30000065':
                        bank_code = '비씨(우리)'
                    if val['BANK_CD'] == '30000066':
                        bank_code = '비씨(하나)'
                    if val['BANK_CD'] == '30000067':
                        bank_code = '비씨(농협)'
                    if val['BANK_CD'] == '30000068':
                        bank_code = '비씨(국민)'
                    if val['BANK_CD'] == '30000069':
                        bank_code = '비씨(신한)'
                    if val['BANK_CD'] == '30000070':
                        bank_code = '비씨(씨티)'
                    if val['BANK_CD'] == '30000071':
                        bank_code = '기타(간이)영수증'

                    '''
    
                            카드타입에 맞게 카드 타입 변경
    
                    '''

                    if val['CARD_TYPE'] == '1':
                        card_type = '법인'
                    if val['CARD_TYPE'] == '2':
                        card_type = '개인'
                    if val['CARD_TYPE'] == '3':
                        card_type = '간이'
                    if val['CARD_TYPE'] == '4':
                        card_type = '교통'
                    if val['CARD_TYPE'] == '5':
                        card_type = '복지'
                    if val['CARD_TYPE'] == '10':
                        card_type = '제로페이'


                    '''
    
                            카드 승인 취소여부 변경
    
                    '''

                    if val['APV_CAN_YN'] == 'A':
                        approve_can = 'approved'
                    if val['APV_CAN_YN'] == 'B':
                        approve_can = 'canceled'

                    # if val['LST_MOD_DT']:
                    #     date = val['LST_MOD_DT']
                    #     write_date = datetime.strptime(val['LST_MOD_DT'], '%Y%m%d%H%M%S')
                    #     _logger.info('------------- %s -----------', val['LST_MOD_DT'])
                        if val['CARD_NO']:
                            val_card_no = val['CARD_NO']

                    backup = i.name
                    card_no = i.card_no

                    if val['CARD_NO'] == i.backup_card_no:
                        code = backup.name
                        backup_card_no = i.backup_card_no
                        _logger.info('---------- code %s ---------', code)
                        _logger.info('---------- backup_card_no %s ---------', i.backup_card_no)
                        _logger.info('------------- %s -----------', val['LST_MOD_DT'])
                        account_id = self.env['account.card.receipts'].create(
                            {
                                "name": env.name,
                                "bank_code": bank_code,
                                "card_no": backup_card_no,
                                "card_no_code": card_no,
                                "expense_state": 'waiting',
                                "approve_no": val['APV_NO'],
                                "approve_can": approve_can,
                                "card_type": card_type,
                                "store_id": val['MEST_NM'],
                                "store_repre_name": val['MEST_REPR_NM'],
                                "store_tele_number": val['MEST_TEL_NO'],
                                "store_address": val['MEST_ADDR_1'],
                                "total": val['BUY_SUM'],
                                "sply_amount": val['SPLY_AMT'],
                                "vat_amount": val['VAT_AMT'],
                                "approve_datetime": write_date,
                                "seq": val['SEQ']
                            }
                        )
                        items.card_state = 'normal'
                        _logger.info('------------- create ----------------')

                    else:
                        items.card_state = 'normal'
                        _logger.info('------------- no create --------------')



    #
    # @api.model
    # def create(self, val):
    #     card_no = self.env['account.card.receipts'].search([])
    #     card_no_list = []
    #     for no in card_no:
    #         card_no_list.append(no.card_no)
    #         _logger.info('----------- list 1 %s -----------', card_no_list)
    #     if card_no_list:
    #         _logger.info('----------- list 2  %s -----------', card_no_list)
    #         split_card = val['card_no']
    #         _logger.info(' self.card_no %s -----', split_card)
    #         str_a = split_card[:4] + "-" + split_card[4:]
    #         str_b = str_a[:9] + "-" + str_a[9:]
    #         str_c = str_b[:14] + "-" + str_b[14:]
    #         val['card_no'] = str_c
    #         res = super(AccountCardReceipts, self).create(val)
    #         return res



    def move_import_expense(self):
        _logger.info(' -- card list view --')
        # receipt_id = self.env['hr.expense'].search(['|', ('name', '=', self.store_id), ('unit_amount', '=', self.total)], limit=1)
        receipt_id = self.env['hr.expense'].search([('seq_id', '=', self.approve_no)], limit=1)

        if receipt_id:
            action = {
                "type": "ir.actions.act_window",
                "name": _("My Expense to Report"),
                "res_model": "hr.expense",
                "view_mode": "tree,form",
                'domain': [('seq_id', '=', self.approve_no)],

            }
            return action

        _logger.info(' --  action receipt view --')


class UnlinkExpense(models.Model):
    _inherit = 'hr.expense'



    def move_receipt(self):
        receipt_id = self.env['account.card.receipts'].search([('approve_no', '=', self.seq_id)], limit=1)
        _logger.info('-------------- name %s ---------------', self.name)

        if receipt_id:
            action = {
                "type": "ir.actions.act_window",
                "name": _("Transaction History"),
                "res_model": "account.card.receipts",
                "view_mode": "tree,form",
                'domain': [('approve_no', '=', self.seq_id)],

            }
            return action

        _logger.info(' --  action receipt view --')


    def unlink(self):
        for expense in self:
            if expense.state in ['draft', 'reported']:
                card_id = self.env['account.card.receipts'].search(['|', ('store_id', '=', expense.name), ('total', '=', expense.unit_amount)])
                for line in card_id:
                    line.expense_state = 'waiting'
                    _logger.info('------------ %s store_id -------------', line.store_id)
                    _logger.info('------------ %s total -------------', line.total)
                    _logger.info('------------ %s  -------------', line)

        super(UnlinkExpense, self).unlink()

    seq_id = fields.Char(string='seq_id')





class ResConfigSettingsProduct(models.TransientModel):
    _inherit = "res.config.settings"

    product_id = fields.Many2one('product.product', string='Default Expense Product')
    module_account_card = fields.Boolean(string='Pb Card')

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsProduct, self).get_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        product_id = ICPSudo.get_param('account_card.product_id')
        _logger.info('----------- product %s ---------', product_id)
        if product_id:
            res.update(
                product_id=int(product_id),

            )
            return res
        else:
            return res


    def set_values(self):
        super(ResConfigSettingsProduct, self).set_values()

        if self.product_id.can_be_expensed == True:
            self.env['ir.config_parameter'].set_param('account_card.product_id', self.product_id.id)
            _logger.info(' ---------------- %s -----------', self.product_id.name)
            _logger.info(' ---------------- %s -----------', self.product_id.can_be_expensed)

