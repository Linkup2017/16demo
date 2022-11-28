# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests
import json
from urllib import parse


import logging
_logger = logging.getLogger(__name__)


class AccountCard(models.Model):
    _inherit = 'res.company'

    name = fields.Char('name')
    connect_card = fields.Boolean(string='Connect Bizplay')
    api_key = fields.Char(string='API Key')
    org_code = fields.Char(string='Org Code')
    connection_state = fields.Selection(
        [("connected", "연결됨"),
         ("error", "오류")],
        string="Connection State", default="error", readonly=True,
    )
    biz_no = fields.Char(string='Business Number')
    card_test = fields.Boolean(string='Is Test ?')
    # product_id = fields.Many2one('product.product', string='Expense default product')
    result_cd = fields.Char('result_cd')

    def send_api(self):
        api_list = []

        API_HOST = "http://webankapi-dev.appplay.co.kr/gateway.do?JSONData="
        method = 'POST'
        headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}
        json_string = {
            "API_ID": "0110",
            "API_KEY": "5a0d6070-1853-4e37-a4b0-fd11e5699296",
            "ORG_CD": "2148635102",
            "REQ_DATA":
                {
                 "BIZ_NO": "2148635102"
                }
        }
        json_Dict = json.dumps(json_string, ensure_ascii=False)
        # json_Dict2 = json.dumps(json_string, ensure_ascii=False, encoding='utf-8')
        JSONData = parse.quote_plus(str(json_Dict))
        url = API_HOST + JSONData
        _logger.info('---------- json_Dict %s --------', json_Dict)
        _logger.info('---------- JSONData %s --------', JSONData)

        # dict = json.dumps(JSONData, indent=2)
        # _logger.info('---------- dict %s --------', dict)
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers
                                     )
        eval_response = eval(response.text)
        api_list.append(eval_response)
        self.result_cd = api_list[0]['RESULT_CD']

        _logger.info("api_list  %s" % api_list)
        _logger.info("self.result_cd   %s" % self.result_cd )
        # _logger.info(list(m['RESULT_MG'] for m in api_list))

        _logger.info(list(m['RESULT_CD'] for m in api_list))


        if api_list[0]['RESULT_CD'] == '00000000':
            self.connection_state = 'connected'
            _logger.info('--------- state %s', self.connection_state)

            return {
                'name': _('Connected'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'bizplay.check',
                'target': 'new',
            }

        if not api_list[0]['RESULT_CD'] == '00000000':
            self.connection_state = 'error'
            _logger.info('--------- state %s', self.connection_state)
            if self.result_cd == 'WFMT0001':
                raise ValidationError(_('수신자료 포맷오류'))
            if self.result_cd == 'WFMT0002':
                raise ValidationError(_('수신자료 변환오류'))
            if self.result_cd == 'WAUT0001':
                raise ValidationError(_('서비스 가능한 이용기관이 아닙니다'))
            if self.result_cd == 'WAUT0003':
                raise ValidationError(_('서비스 설정 값이 잘못되었습니다'))
            if self.result_cd == 'WAUT0004':
                raise ValidationError(_('인증키 만료'))
            if self.result_cd == 'WAUT0005':
                raise ValidationError(_('인증키 미사용'))
            if self.result_cd == 'WAUT0006':
                raise ValidationError(_('인증키 사용정지'))
            if self.result_cd == 'WAUT0007':
                raise ValidationError(_('잘못된 인증키'))
            if self.result_cd == 'WAUT0008':
                raise ValidationError(_('알수 없는 인증키'))
            if self.result_cd == 'WAUT0009':
                raise ValidationError(_('IP 체크여부 오류'))
            if self.result_cd == 'WAUT0010':
                raise ValidationError(_('인증키 미입력'))
            if self.result_cd == 'WAUT0011':
                raise ValidationError(_('해당 사업자번호는 비즈플레이 경비관리 미사용 고객입니다'))
            if self.result_cd == 'WPAR0001':
                raise ValidationError(_('잘못된 API ID 입니다'))
            if self.result_cd == 'WPAR0002':
                raise ValidationError(_('입력값 오류'))
            if self.result_cd == 'WPAR0003':
                raise ValidationError(_('필수 입력값 미입력'))
            if self.result_cd == 'WSND0001':
                raise ValidationError(_('결과 처리 중 오류가 발생하였습니다'))
            if self.result_cd == 'WSND0002':
                raise ValidationError(_('전문 응답 값 오류 입니다.'))
            if self.result_cd == 'WERR0001':
                raise ValidationError(_('파일 오류'))
            if self.result_cd == 'WERR0002':
                raise ValidationError(_('수신자료 처리 중 오류'))
            if self.result_cd == 'WERR0003':
                raise ValidationError(_('기타 오류'))
            if self.result_cd == 'WERR0005':
                raise ValidationError(_('서버 연결 오류'))
        else:
            raise ValidationError(_('%s 오류 입니다.', self.result_cd))



