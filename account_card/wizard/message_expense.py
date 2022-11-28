from odoo import _, api, exceptions, fields, models
from popbill import EasyFinBankService, PopbillException, ContactInfo, JoinForm, CorpInfo, BankAccountInfo
from datetime import datetime, timedelta
import json
import requests
from urllib import parse

import logging
_logger = logging.getLogger(__name__)


class CheckPopupMessage(models.TransientModel):
    _name = 'expense.check'

    name = fields.Char('')

