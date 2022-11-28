odoo.define('pos_inicis.models', function (require) {
    
const { register_payment_method, Payment } = require('point_of_sale.models');
const PaymentInicis = require('pos_inicis.payment');
const Registries = require('point_of_sale.Registries');

register_payment_method('inicis', PaymentInicis);

const PosInicisPayment = (Payment) => class PosInicisPayment extends Payment {
    constructor(obj, options) {
        super(...arguments);
        this.monthly_installment = this.monthly_installment || 0;
    }
    //@override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.monthly_installment = this.monthly_installment;
        return json;
    }
    //@override
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.monthly_installment = json.monthly_installment;
    }
    get_monthly_installment() {
        return this.monthly_installment;
    }
    set_monthly_installment(value) {
        this.monthly_installment = value;
    }
    get_transaction_id(){
        return this.transaction_id;
    }
    set_transaction_id(value){
        this.transaction_id = value;
    }
    export_for_printing() {
        var json = super.export_for_printing(...arguments);
        json.transaction_id =  this.transaction_id;
        return json;
    }
}
Registries.Model.extend(Payment, PosInicisPayment);
});
