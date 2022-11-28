odoo.define('web.LinkupApprovalFormController', function (require) {
"use strict";

var FormController = require('web.FormController');
var core = require('web.core');


var ApprovalFormController = FormController.include({

    renderButtons: function ($node) {
       console.log('----renderButtons----')
       console.log(this)

       this._super.apply(this, arguments);
       if(this.modelName === "kapprove.doc")
       {
           $("div.o_form_button_create").hide();
       }
    },

});

});
