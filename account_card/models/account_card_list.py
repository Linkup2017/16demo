# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests
import json
from urllib import parse
from datetime import datetime, timedelta
import re


import logging
_logger = logging.getLogger(__name__)

class AccountCardList(models.Model):
    _name = 'account.card'
    _inherit = ["mail.thread"]

    name = fields.Many2one('res.bank.list', string='Card bank Code', required=True, domain="[('type_selection', '=', 'card')]")
    # name = fields.Many2one('account.card.no', string='Card bank Code', required=True)
    card_no = fields.Char(string='Card number', required=True)
    backup_card_no = fields.Char(string='Card Back Number')
    card_nk_name = fields.Char(string='Card nick name')
    employee_id = fields.Many2one('res.partner', string='Employee')
    responsible_id = fields.Many2one('hr.employee', string='Responsible')
    card_state = fields.Selection([('normal', '정상'),
                                   ('termination', '해지'),
                                   ('check', '확인중')],
                                  string='Card State', readonly=True, default='check')
    user_id = fields.Many2one('hr.employee', string='User')
    company_id = fields.Many2one('res.company', string='Company Name', required=True, default=lambda self: self.env.company)
    edi_state = fields.Char(string='EDI card state')
    line_test_id = fields.Many2one('account.card.receipts')
    note = fields.Text(string='Description')

    def check_card(self):

        item = self.env['res.company'].search([('connect_card', '=', True)])
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

        if response.status_code == 200:
            self.card_state = 'normal'

    def unconnect_button(self):
        self.card_state = 'check'



    @api.model
    def create(self, val):
        card_no = self.env['account.card'].search([])
        card_no_list =[]
        for no in card_no:
            card_no_list.append(no.backup_card_no)
            _logger.info('----------- list 1 %s -----------', card_no_list)

        if val.get('card_no') not in card_no_list:
            _logger.info('----------- val %s -----------', val.get('card_no'))
            _logger.info('----------- list 2  %s -----------', card_no_list)
            split_card = val['card_no']
            if split_card:
                new_card = split_card[0:4] + '********' + split_card[12:16]
                _logger.info('------- %s new_card ---', new_card)
            _logger.info('----------- split_card len  %s -----------', len(split_card))

            val['backup_card_no'] = val['card_no']
            str_a = new_card[:4] + "-" + new_card[4:]
            str_b = str_a[:9] + "-" + str_a[9:]
            str_c = str_b[:14] + "-" + str_b[14:]
            test_list = str.split('-')
            _logger.info('------------ test %s ------------', test_list)
            val['card_no'] = str_c
            val['backup_card_no'] = split_card
            _logger.info(' val %s -----', val['backup_card_no'])
            res = super(AccountCardList, self).create(val)
            return res
        else:
            raise ValidationError(_('카드번호 중복'))

    def write(self, val):
        card_no = self.env['account.card'].search([])
        card_no_list =[]
        for no in card_no:
            card_no_list.append(no.backup_card_no)
            _logger.info('----------- list 1 %s -----------', card_no_list)

        if val.get('card_no') not in card_no_list:
            _logger.info('----------- val %s -----------', val.get('card_no'))
            _logger.info('----------- list 2  %s -----------', card_no_list)
            split_card = val['card_no']
            if split_card:
                new_card = split_card[0:4] + '********' + split_card[12:16]
                _logger.info('------- %s new_card ---', new_card)
            _logger.info('----------- split_card len  %s -----------', len(split_card))

            val['backup_card_no'] = val['card_no']
            str_a = new_card[:4] + "-" + new_card[4:]
            str_b = str_a[:9] + "-" + str_a[9:]
            str_c = str_b[:14] + "-" + str_b[14:]
            test_list = str.split('-')
            _logger.info('------------ test %s ------------', test_list)
            val['card_no'] = str_c
            val['backup_card_no'] = split_card
            _logger.info(' val %s -----', val['backup_card_no'])

            _logger.info('---------- %s ------------', val)
            res = super(AccountCardList, self).write(val)
            return res
        else:
            raise ValidationError(_('카드번호 중복'))



    # def send_api(self):
    #     api_list = []
    #     API_HOST = "http://webankapi-dev.appplay.co.kr/gateway.do?JSONData="
    #     method = 'POST'
    #     headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}
    #     json_string = {
    #         "API_ID": "0210",
    #         "API_KEY": "5a0d6070-1853-4e37-a4b0-fd11e5699296",
    #         "ORG_CD": "2148635102",
    #         "REQ_DATA":
    #             {
    #                 "BIZ_NO": "2148635102"
    #             }
    #     }
    #     json_Dict = json.dumps(json_string, ensure_ascii=False)
    #     JSONData = parse.quote_plus(str(json_Dict))
    #     url = API_HOST + JSONData
    #
    #     try:
    #         if method == 'GET':
    #             response = requests.get(url, headers=headers)
    #         elif method == 'POST':
    #             response = requests.post(url, headers=headers)
    #         _logger.info("response status %r" % response.status_code)
    #
    #         eval_response = response.text
    #         to_json = json.loads(eval_response)
    #         _logger.info('------- to_json %s -----------', type(to_json))
    #
    #         # api_list.append(eval_response)
    #         # _logger.info('------- api list %s -----------', api_list)
    #
    #
    #     except Exception as ex:
    #         print(ex)
    #
    #     return response


    def action_card_search(self):
        api_list = []
        API_HOST = "http://webankapi-dev.appplay.co.kr/gateway.do?JSONData="
        method = 'POST'
        headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}
        json_string = {
            "API_ID": "0210",
            "API_KEY": "5a0d6070-1853-4e37-a4b0-fd11e5699296",
            "ORG_CD": "2148635102",
            "REQ_DATA":
                {
                    "BIZ_NO": "2148635102"
                }
        }
        json_Dict = json.dumps(json_string, ensure_ascii=False)
        JSONData = parse.quote_plus(str(json_Dict))
        url = API_HOST + JSONData

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers)
            _logger.info("response status %r" % response.status_code)

            eval_response = response.text
            to_json = json.loads(eval_response)
            _logger.info('------- to_json %s -----------', type(to_json))
            _logger.info('------- to_json %s -----------', to_json['RES_DATA'])
            # api_list.append(eval_response)
            # _logger.info('------- api list %s -----------', api_list)


        except Exception as ex:
            print(ex)

        return response

    # def action_import_receipt_item(self):
    #
    #     items = self.env["account.card.receipts"].search([("bank_code", '!=', None)])
    #     _logger.info('------------------ items items %s ---------------', items)
    #     return self.action_import_receipt(items)
    #
    # def action_import_receipt(self, items):
    #     item = self.env['res.company'].search([('connect_card', '=', True)])
    #     list_id = self.env['account.card'].search([])
    #
    #     api_list = []
    #     approve_no_list = []
    #     for li in items:
    #         approve_no_list.append(li.approve_no)
    #     # _logger.info('----------- %approve_no_list -------- ', approve_no_list)
    #
    #
    #     for value in item:
    #         for env in list_id:
    #             _logger.info('---------------- val %s ---------', env.backup_card_no)
    #             _logger.info('--------- %s i --------', value)
    #             API_HOST = "http://webankapi-dev.appplay.co.kr/gateway.do?JSONData="
    #             method = 'POST'
    #             headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}
    #             json_string = {
    #                 "API_ID": "0410",
    #                 "API_KEY": value.api_key,
    #                 "ORG_CD": value.org_code,
    #                 "REQ_DATA": {
    #                     "BIZ_NO": value.biz_no,
    #                     "CARD_NO": "",
    #                     "START_DATE": "20161101",
    #                     "START_TIME": "",
    #                     "END_DATE": "20161130",
    #                     "END_TIME": "",
    #                     "REQ_CNT": "",
    #                     "APV_CAN_YN": "",
    #                     "NEXT_KEY": ""
    #                 }
    #             }
    #             json_Dict = json.dumps(json_string, ensure_ascii=False)
    #             JSONData = parse.quote_plus(str(json_Dict))
    #             url = API_HOST + JSONData
    #
    #             if method == 'GET':
    #                 response = requests.get(url, headers=headers)
    #             elif method == 'POST':
    #                 response = requests.post(url, headers=headers)
    #             _logger.info("response status %r" % response.status_code)
    #
    #             eval_response = response.text
    #             to_json = json.loads(eval_response)
    #             _logger.info('-------- %s -------', eval_response)
    #             for li in to_json['RES_DATA']:
    #                 api_list.append(li['APV_NO'])
    #
    #             for val in to_json['RES_DATA']:
    #                 if not val:
    #                     _logger.info('-- ? --')
    #                     self.card_state = 'termination'
    #                     _logger.info('--------------------- %s val -----------------', val['SEQ'])
    #                 if val['APV_NO'] not in str(approve_no_list):
    #                     _logger.info('---------------- %s val --------------', val)
    #                     # _logger.info('---------------- %s approve_no_list --------------', approve_no_list)
    #                     _logger.info('---------------- %s api_list --------------', val['APV_NO'])
    #
    #                     '''
    #
    #                      카드사 코드번호에 맞게 카드사 이름 변경
    #
    #                     '''
    #
    #                     if val['BANK_CD'] == '30000001':
    #                         bank_code = 'KB'
    #                     if val['BANK_CD'] == '30000002':
    #                         bank_code = '현대'
    #                     if val['BANK_CD'] == '30000003':
    #                         bank_code = '삼성'
    #                     if val['BANK_CD'] == '30000004':
    #                         bank_code = '외환'
    #                     if val['BANK_CD'] == '30000006':
    #                         bank_code = '비씨'
    #                     if val['BANK_CD'] == '30000008':
    #                         bank_code = '신한'
    #                     if val['BANK_CD'] == '30000010':
    #                         bank_code = '하나'
    #                     if val['BANK_CD'] == '30000012':
    #                         bank_code = '광주'
    #                     if val['BANK_CD'] == '30000013':
    #                         bank_code = '수협'
    #                     if val['BANK_CD'] == '30000014':
    #                         bank_code = '전북'
    #                     if val['BANK_CD'] == '30000015':
    #                         bank_code = '하나'
    #                     if val['BANK_CD'] == '30000016':
    #                         bank_code = '씨티'
    #                     if val['BANK_CD'] == '30000017':
    #                         bank_code = '아맥스(롯데)'
    #                     if val['BANK_CD'] == '30000018':
    #                         bank_code = '우리'
    #                     if val['BANK_CD'] == '30000019':
    #                         bank_code = '롯데(개인카드)'
    #                     if val['BANK_CD'] == '30000020':
    #                         bank_code = '산은'
    #                     if val['BANK_CD'] == '30000021':
    #                         bank_code = 'NH'
    #                     if val['BANK_CD'] == '30000060':
    #                         bank_code = '비씨(기업)'
    #                     if val['BANK_CD'] == '30000061':
    #                         bank_code = '비씨(SC)'
    #                     if val['BANK_CD'] == '30000062':
    #                         bank_code = '비씨(부산)'
    #                     if val['BANK_CD'] == '30000063':
    #                         bank_code = '비씨(대구)'
    #                     if val['BANK_CD'] == '30000064':
    #                         bank_code = '비씨(경남)'
    #                     if val['BANK_CD'] == '30000065':
    #                         bank_code = '비씨(우리)'
    #                     if val['BANK_CD'] == '30000066':
    #                         bank_code = '비씨(하나)'
    #                     if val['BANK_CD'] == '30000067':
    #                         bank_code = '비씨(농협)'
    #                     if val['BANK_CD'] == '30000068':
    #                         bank_code = '비씨(국민)'
    #                     if val['BANK_CD'] == '30000069':
    #                         bank_code = '비씨(신한)'
    #                     if val['BANK_CD'] == '30000070':
    #                         bank_code = '비씨(씨티)'
    #                     if val['BANK_CD'] == '30000071':
    #                         bank_code = '기타(간이)영수증'
    #
    #                     '''
    #
    #                             카드타입에 맞게 카드 타입 변경
    #
    #                     '''
    #
    #                     if val['CARD_TYPE'] == '1':
    #                         card_type = '법인'
    #                     if val['CARD_TYPE'] == '2':
    #                         card_type = '개인'
    #                     if val['CARD_TYPE'] == '3':
    #                         card_type = '간이'
    #                     if val['CARD_TYPE'] == '4':
    #                         card_type = '교통'
    #                     if val['CARD_TYPE'] == '5':
        #                         card_type = '복지'
        #                     if val['CARD_TYPE'] == '10':
    #                         card_type = '제로페이'
    #
    #
    #                     '''
    #
    #                             카드 승인 취소여부 변경
    #
    #                     '''
    #
    #                     if val['APV_CAN_YN'] == 'A':
    #                         approve_can = 'approved'
    #                     if val['APV_CAN_YN'] == 'B':
    #                         approve_can = 'canceled'
    #
    #                     if val['LST_MOD_DT']:
    #                         date = val['LST_MOD_DT']
    #                         write_date = datetime.strptime(date, '%Y%m%d%H%M%S')
    #                     if val['CARD_NO']:
    #                         account_id = self.env['account.card.receipts'].create(
    #                             {
    #                                 "name": env.name,
    #                                 "bank_code": bank_code,
    #                                 "card_no": val['CARD_NO'],
    #                                 "expense_state": 'waiting',
    #                                 "approve_no": val['APV_NO'],
    #                                 "approve_can": approve_can,
    #                                 "card_type": card_type,
    #                                 "store_id": val['MEST_NM'],
    #                                 "store_repre_name": val['MEST_REPR_NM'],
    #                                 "store_tele_number": val['MEST_TEL_NO'],
    #                                 "store_address": val['MEST_ADDR_1'],
    #                                 "total": val['BUY_SUM'],
    #                                 "sply_amount": val['SPLY_AMT'],
    #                                 "vat_amount": val['VAT_AMT'],
    #                                 "employee_id": env.employee_id.id,
    #                                 "approve_datetime": write_date,
    #                                 "seq": val['SEQ']
    #                             }
    #                         )
    #                     self.card_state = 'normal'
    #                     _logger.info('------------- employee_id %s --------', self.employee_id)
    #                     _logger.info('------------- create ----------------')
    #                 else:
    #                     self.card_state = 'normal'
    #                     _logger.info('------------- no create -------------- ')

    def move_import_receipt(self):
        receipt_id = self.env['account.card.receipts'].search([('bank_code', '=', self.name.name)], limit=1)
        _logger.info('-------------- receipt %s ---------------', receipt_id.bank_code)
        _logger.info('-------------- name %s ---------------', self.name.name)

        if receipt_id:
            action = {
                "type": "ir.actions.act_window",
                "name": _("Transaction History"),
                "res_model": "account.card.receipts",
                "view_mode": "tree,form",
                'domain': [('bank_code', '=', self.name.name)],

            }
            return action

        _logger.info(' --  action receipt view --')

    def move_card_list(self):
        _logger.info(' -- card list view --')


