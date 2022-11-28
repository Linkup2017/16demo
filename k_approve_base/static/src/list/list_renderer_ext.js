odoo.define('web.ApprovalListRenderer', function (require) {
"use strict";

var ListRenderer = require('web.ListRenderer');
var core = require('web.core');
var _t = core._t;
var qweb = core.qweb;

var DocListRenderer = ListRenderer.include({


  _renderHeader: function () {
      if(this.state.model === 'kapproval.product.line') {
         console.log('--_renderHeader--');
         this.state.fields.product_id.string = this.__parentedParent.recordData.str_has_product;
         this.state.fields.amount.string = this.__parentedParent.recordData.str_has_amount;
         this.state.fields.quantity.string = this.__parentedParent.recordData.str_has_quantity;
         this.state.fields.description.string = this.__parentedParent.recordData.str_has_description;
      }
      return this._super.apply(this, arguments);
  },

});

});
