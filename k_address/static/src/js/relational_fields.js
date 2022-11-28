odoo.define('kaddress_form.relational_fields', function (require) {
"use strict";

var {FieldMany2One,M2ODialog} = require('web.relational_fields');

var kaddressFieldMany2One = FieldMany2One.include({

     events: _.extend({}, FieldMany2One.prototype.events, {
        'inputcomplete': '_onInputcomplete',
     }),
     _onInputcomplete : function (event) {
        console.log('--_onInputcomplete---')
        var value = this.$input.val()
        var value_id = this.$input.data("value_id");
        var value_name = this.$input.data("value_name");
        this.reinitialize({id: value_id, display_name: value_name});
     },

});


});
