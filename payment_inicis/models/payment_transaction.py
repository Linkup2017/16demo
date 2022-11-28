# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import hashlib
import time
import datetime
import requests
from odoo.http import request
import socket

from werkzeug import urls


from odoo import _, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_repr, float_round

from odoo.addons.payment_inicis.controllers.main import PaymentInicisController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    payMethod = fields.Char(string='payMethod Type')

    def _get_signature(self, oid, price, timestamp):
        sig_data = {
            'oid': oid,
            'price': price,
            'timestamp': timestamp,
        }
        sig_data_string = '&'.join(['{}={}'.format(k, v) for k, v in sig_data.items()])
        return hashlib.sha256(sig_data_string.encode('utf-8')).hexdigest()

    def _re_get_signature(self, authToken, timestamp):
        sig_data = {
            'authToken': authToken,
            'timestamp': timestamp,
        }
        sig_data_string = '&'.join(['{}={}'.format(k, v) for k, v in sig_data.items()])
        return hashlib.sha256(sig_data_string.encode('utf-8')).hexdigest()


    def _get_hashdata(self, INIAPIKey, type, paymethod, mid, tid, clientIp, timestamp):
        sig_data = {
            'INIAPIKey': INIAPIKey,
            'type': type,
            'paymethod': paymethod,
            'clientIp ': clientIp,
            'mid': mid,
            'tid': tid,
            'timestamp': timestamp,
        }
        sig_data_string = '&'.join(['{}={}'.format(k, v) for k, v in sig_data.items()])
        return hashlib.sha512(sig_data_string.encode('utf-8')).hexdigest()



    def _get_timestamp(self):
        d = datetime.datetime.now()
        t = time.mktime(d.timetuple())
        return '%d%d' % (t, d.microsecond / 1000)

    def _get_mKey(self):
        return hashlib.sha256(self.provider_id.inicis_sign_key.encode('utf-8')).hexdigest()

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Alipay-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'inicis':
            return res

        base_url = self.provider_id.get_base_url()
        _logger.info('----- base url % s -----', base_url)
        so = self.sale_order_ids[0]
        oid = self.reference
        timestamp = self._get_timestamp()
        currency = 'WON' if self.currency_id.name == 'USD' else self.currency_id.name
        price = float_repr(float_round(self.amount, 2) * 100, 0) if currency == 'USD' else float_repr(self.amount, 0)
        rendering_values = dict(
            version='1.0',
            mid=self.provider_id.inicis_mid,
            oid=oid,
            goodname=so.order_line[0].display_name if so and so.order_line else '',
            quantity=len(so.order_line),
            price=price,
            tax='0',
            taxfree='0',
            currency=currency,
            buyername=self.partner_id.name,
            buyertel=self.partner_id.phone,
            buyeremail=self.partner_id.email,
            timestamp=timestamp,
            signature=self._get_signature(oid, price, timestamp),
            returnUrl=urls.url_join(base_url, PaymentInicisController._return_url),
            mKey=self._get_mKey(),
            closeUrl=urls.url_join(base_url, '/payment/inicis/close'),
        )

        return rendering_values

    #=== BUSINESS METHODS ===#

    def _send_payment_request(self):
        """ Override of payment to simulate a payment request.

        Note: self.ensure_one()

        :return: None
        """
        super()._send_payment_request()
        if self.provider_code != 'inicis':
            return

        if not self.token_id:
            raise UserError("Inicis: " + _("The transaction is not linked to a token."))

        notification_data = {'reference': self.reference, 'state': 'done'}
        self._handle_notification_data('inicis', notification_data)

    def _send_refund_request(self, amount_to_refund=None):
        """ Override of payment to simulate a refund.
            INICIS 환불 요청 부분
        Note: self.ensure_one()

        :param dict kwargs: The keyword arguments.
        :return: The refund transaction created to process the refund request.
        :rtype: recordset of `payment.transaction`
        """
        refund_tx = super()._send_refund_request(amount_to_refund=amount_to_refund)
        if self.provider_code != 'inicis':
            return refund_tx

        d = datetime.datetime.now()
        timestamp = d.strftime('%Y%m%d%H%M%S')
        hostname = request.httprequest.host.split(':')[0]
        clientIp = socket.gethostbyname(hostname)
        refund_url = 'https://%s.inicis.com/api/v1/refund' % (
            'inicis' if self.provider_id.state == 'enabled' else 'stginiapi')
        tid = self.provider_reference
        type = 'Refund'
        # paymethod = self.payMethod
        paymethod = 'Card'
        mid = self.provider_id.inicis_mid
        msg = "취소요청"
        values = dict(
            type=type,
            paymethod=paymethod,
            timestamp=timestamp,
            clientIp=clientIp,
            mid=mid,
            tid=tid,
        )

        if not self.provider_id.inicis_sign_key:
            raise UserError(_("Please configure the INIpay acquirer's Merchant ID Key."))
        data = self.provider_id.inicis_mid_key + ''.join([v for k, v in values.items()])
        _logger.info('refund_url %s ', refund_url)
        _logger.info('data:\n%s', data)
        hashdata = hashlib.sha512(data.encode('utf-8')).hexdigest()
        values = dict(
            values,
            msg=msg,
            hashData=hashdata
        )
        _logger.info('_request_inicis_refund: Sending values to inicis URL, values:\n%s', pprint.pformat(values))
        try:
            response = requests.post(refund_url, data=values)
            _logger.info('response (HTTP status %s):\n%s', response.status_code, response.text)
            _logger.info('response data:\n%s', response.json())
            response.json()
        except Exception as e:
            raise e
        #
        # notification_data = {'reference': refund_tx.reference, 'state': 'done'}
        # refund_tx._handle_notification_data('inicis', notification_data)
        #
        # return refund_tx


    def _send_capture_request(self):
        """ Override of payment to simulate a capture request.

        Note: self.ensure_one()

        :return: None
        """
        super()._send_capture_request()
        if self.provider_code != 'inicis':
            return

        notification_data = {
            'reference': self.reference,
            'simulated_state': 'done',
            'manual_capture': True,  # Distinguish manual captures from regular one-step captures.
        }
        self._handle_notification_data('inicis', notification_data)

    def _send_void_request(self):
        """ Override of payment to simulate a void request.

        Note: self.ensure_one()

        :return: None
        """
        super()._send_void_request()
        if self.provider_code != 'inicis':
            return

        notification_data = {'reference': self.reference, 'simulated_state': 'cancel'}
        self._handle_notification_data('inicis', notification_data)

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on dummy data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The dummy notification data
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'inicis' or len(tx) == 1:
            return tx

        # reference = notification_data.get('merchant_reference')
        reference = notification_data.get('orderNumber')
        if not reference:
            raise ValidationError(
                "Inicis: " + _("Received data with missing reference %(ref)s.", ref=reference)
            )

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'inicis')])
        if not tx:
            raise ValidationError(
                "Inicis: " + _("No transaction found matching reference %s.", reference)
            )

        return tx


    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on dummy data.

        Note: self.ensure_one()

        :param dict notification_data: The dummy notification data
        :return: None
        :raise: ValidationError if inconsistent data were received
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'inicis':
            return

        if self.tokenize:
            # The reasons why we immediately tokenize the transaction regardless of the state rather
            # than waiting for the payment method to be validated ('authorized' or 'done') like the
            # other payment providers do are:
            # - To save the simulated state and payment details on the token while we have them.
            # - To allow customers to create tokens whose transactions will always end up in the
            #   said simulated state.
            self._inicis_tokenize_from_notification_data(notification_data)

        state = notification_data

        currency = 'WON' if self.currency_id.name == 'USD' else self.currency_id.name
        price = float_repr(float_round(self.amount, 2) * 100, 0) if currency == 'USD' else float_repr(self.amount, 0)
        resultCode = notification_data['resultCode']

        if resultCode != '0000':
            self._set_pending()
        elif resultCode == '0000':
            timestamp = self._get_timestamp()
            authToken = notification_data.get('authToken')
            authUrl = notification_data.get('authUrl')

            values = dict(
                mid=notification_data.get('mid'),
                authToken=authToken,
                timestamp=timestamp,
                signature=self._re_get_signature(authToken, timestamp),
                charset='UTF-8',
                format='JSON',
                price=price,
            )
            try:
                response = requests.post(authUrl, data=values)
                _logger.info('response (HTTP status %s):\n%s', response.status_code, response.text)
                _logger.info('response data:\n%s', response.json())
                notification_data.update(response.json())
            except Exception as e:
                raise e
            self.payMethod = notification_data.get('payMethod')
            result = notification_data.get('resultCode')
            self.provider_reference = notification_data.get('tid')

            if result != '0000':
                self._set_authorized()
            else:
                self._set_done()
                # Immediately post-process the transaction if it is a refund, as the post-processing
                # will not be triggered by a customer browsing the transaction from the portal.
                if self.operation == 'refund':
                    self.env.ref('payment.cron_post_process_payment_tx')._trigger()

        elif state == 'cancel':
            self._set_canceled()
        else:  # Simulate an error state.
            self._set_error(_("You selected the following inicis payment status: %s", state))
        return values

    def _inicis_tokenize_from_notification_data(self, notification_data):
        """ Create a new token based on the notification data.

        Note: self.ensure_one()

        :param dict notification_data: The fake notification data to tokenize from.
        :return: None
        """
        self.ensure_one()

        state = notification_data
        applNum = notification_data.get('applNum')
        token = self.env['payment.token'].create({
            'provider_id': self.provider_id.id,
            'payment_details': notification_data['payment_details'],
            'partner_id': self.partner_id.id,
            'provider_ref': applNum,
            'verified': True,
            'inicis_simulated_state': state,
        })
        self.write({
            'token_id': token,
            'tokenize': False,
        })
        _logger.info(
            "Created token with id %s for partner with id %s.", token.id, self.partner_id.id
        )
