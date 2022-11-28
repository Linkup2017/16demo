/* global INIStdPay */
odoo.define('payment_inicis.payment_form', require => {
    'use strict';

    const core = require('web.core');


    const { loadJS } = require('@web/core/assets');
    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');

    const _t = core._t;


    const inicisMixin = {

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Simulate a feedback from a payment provider and redirect the customer to the status page.
         *
         * @override method from payment.payment_form_mixin
         * @private
         * @param {string} code - The code of the provider
         * @param {number} providerId - The id of the provider handling the transaction
         * @param {object} processingValues - The processing values of the transaction
         * @return {Promise}
         */
        _processRedirectPayment: function (code, providerId, processingValues) {
            if (code !== 'inicis') {
                return this._super(...arguments);
            }

            const $redirectForm = $(processingValues.redirect_form_html).attr(
                'id', 'SendPayForm_id'
            );

            // Ensures external redirections when in an iframe.
            $redirectForm[0].setAttribute('target', '_top');
            $(document.getElementsByTagName('body')[0]).append($redirectForm);

            INIStdPay.pay('SendPayForm_id');
        },

        /**
         * Prepare the inline form of Inicis for direct payment.
         *
         * @override method from payment.payment_form_mixin
         * @private
         * @param {string} code - The code of the selected payment option's provider
         * @param {integer} paymentOptionId - The id of the selected payment option
         * @param {string} flow - The online payment flow of the selected payment option
         * @return {Promise}
         */
        _prepareInlineForm: function (code, paymentOptionId, flow) {
            if (code !== 'inicis') {
                return this._super(...arguments);
            } else if (flow === 'token') {
                return Promise.resolve();
            }
            this._setPaymentFlow('redirect');

            let INIStdPayJSUrl = 'https://stdpay.inicis.com/stdjs/INIStdPay.js';
            return this._rpc({
                route: '/payment/inicis/get_provider_info',
                params: {
                    'provider_id': paymentOptionId,
                },
            }).then(providerInfo => {
                if (providerInfo.state !== 'enabled') {
                    INIStdPayJSUrl = 'https://stgstdpay.inicis.com/stdjs/INIStdPay.js';
                }
                this.inicisInfo = providerInfo;
            }).then(() => {
                loadJS(INIStdPayJSUrl);
            }).guardedCatch((error) => {
                error.event.preventDefault();
                this._displayError(
                    _t("Server Error"),
                    _t("An error occurred when displayed this payment form."),
                    error.message.data.message
                );
            });
        },


    };
    checkoutForm.include(inicisMixin);
    manageForm.include(inicisMixin);
});
