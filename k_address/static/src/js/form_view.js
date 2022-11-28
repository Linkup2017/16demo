odoo.define('k_address.FollowupFormView', function (require) {
"use strict";

/**
 * FollowupFormView
 *
 * The FollowupFormView is a sub-view of FormView. It's used to display
 * the Follow-up reports, and manage the complete flow (send by mail, send
 * letter, ...).
 */


var FormView = require('web.FormView');
var viewRegistry = require('web.view_registry');

var FollowupFormView = FormView.extend({
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        console.log('--FollowupFormView----')
    },

});

viewRegistry.add('kaddress_form', FollowupFormView);

return FollowupFormView;
});