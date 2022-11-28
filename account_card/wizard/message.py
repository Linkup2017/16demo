from odoo import _, api, exceptions, fields, models
from popbill import EasyFinBankService, PopbillException, ContactInfo, JoinForm, CorpInfo, BankAccountInfo
from datetime import datetime, timedelta
import json
import requests
from urllib import parse

import logging
_logger = logging.getLogger(__name__)


class CheckPopupMessage(models.TransientModel):
    _name = 'bizplay.check'

    def _default_status(self):
        check_company_id = self.env['res.company'].search(["id", '=', self.company_id.id], limit=1)
        if check_company_id:
            _logger.info('------------ %s ---------', check_company_id)
            if check_company_id.connection_state == 'connect':
                self.check_connect = 'Connect Successfully !'


    check_connect = fields.Char(dafault=_default_status, readonly=True)
    check_failed = fields.Char(string='Failed Connect ..')
    company_id = fields.Many2one('res.company')


