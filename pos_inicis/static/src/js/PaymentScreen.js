odoo.define('pos_inicis.PaymentScreen', function(require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { onMounted } = owl;

    const PosInicisPaymentScreen = PaymentScreen =>class extends PaymentScreen {

        async _sendPaymentRequest({ detail: line }) {
            if ( line.payment_method.use_payment_terminal !== 'inicis' ) {
                return super._sendPaymentRequest(...arguments);
            }

            if ( line.get_amount() > 0 ) {
                const {confirmed, payload: inputNumber} = await this.showPopup('NumberInputPopup', {
                    title: this.env._t('Enter Monthly Installments'),
                    startingValue: line.get_monthly_installment(),
                });
                if (confirmed) {
                    line.set_monthly_installment(inputNumber);
                    return super._sendPaymentRequest(...arguments);
                }
            }
            else {
                const {confirmed, payload: approvalNumber} = await this.showPopup('NumberInputPopup', {
                    title: this.env._t('Enter Approval Number'),
                    startingValue: line.get_transaction_id(),
                });
                if (confirmed) {
                    line.set_transaction_id(approvalNumber);
                    return super._sendPaymentRequest(...arguments);
                }
            }
        }
    };

    Registries.Component.extend(PaymentScreen, PosInicisPaymentScreen);

    return PaymentScreen;
});
