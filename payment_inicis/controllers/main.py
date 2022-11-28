# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug


from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError




_logger = logging.getLogger(__name__)


class PaymentInicisController(http.Controller):
    _return_url = '/payment/inicis/return'
    _webhook_url = '/payment/inicis/webhook'




    @http.route('/payment/inicis/get_provider_info', type='json', auth='public', csrf=False)
    def inicis_get_provider_info(self, provider_id):
        """ Return public information on the provider.

        :param int provider_id: The provider handling the transaction, as a `payment.provider` id

        :return: Information on the provider, namely: the state

        :rtype: dict
        """

        _logger.info("Handling redirection from APS with data:\n%s",
                     pprint.pformat(provider_id))  # Check the integrity of the notification.


        provider_sudo = request.env['payment.provider'].sudo().browse(provider_id).exists()
        return {
            'state': provider_sudo.state,

        }

    @http.route(_return_url, type='http',  methods=['POST'], auth='public', csrf=False,  save_session=False)
    def inicis_return(self, **data):

        _logger.info("Handling redirection from INIcis with data:\n%s", pprint.pformat(data))  # Check the integrity of the notification.
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
            'inicis', data
        )

        # Handle the notification data.
        tx_sudo._handle_notification_data('inicis', data)
        return request.redirect('/payment/status')


    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def inicis_webhook(self, **data):
        """ Process the notification data sent by INIcis to the webhook.
        :param dict data: The notification data.
        :return: The 'SUCCESS' string to acknowledge the notification
        :rtype: str
        """
        _logger.info("Notification received from APS with data:\n%s", pprint.pformat(data))
        try:
            # Check the integrity of the notification.
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
                'inicis', data
            )
            self._verify_notification_signature(data, tx_sudo)

            # Handle the notification data.
            tx_sudo._handle_notification_data('inicis', data)
        except ValidationError:  # Acknowledge the notification to avoid getting spammed.
            _logger.exception("Unable to handle the notification data; skipping to acknowledge.")

        return ''  # Acknowledge the notification.
