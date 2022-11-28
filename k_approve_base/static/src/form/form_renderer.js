odoo.define('web.ApprovalFormRenderer1', function (require) {
"use strict";

var FormRenderer = require('web.FormRenderer');

var core = require('web.core');
var _t = core._t;
var qweb = core.qweb;


var DocFormRenderer = FormRenderer.include({

    getSeqnumberFromStateData :function (node) {

        var seq = 0;

        if (node.attrs.modifiers && node.attrs.modifiers.invisible)
        {
            if(Array.isArray(node.attrs.modifiers.invisible)) {
                var data = node.attrs.modifiers.invisible[0];
                if(node.attrs.modifiers.invisible.length > 1)
                {
                    data = node.attrs.modifiers.invisible[1];
                }
                var sdata = data[0];

                if (sdata === 'has_partners') {
                    seq = this.state.data.number_has_partners;
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_partners);

                    }
                    this.state.fields.partner_ids.string = _t(this.state.data.str_has_partners);
                }
                else if (sdata === 'has_amount') {
                    seq = this.state.data.number_has_amount;
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_amount);
                    }
                    this.state.fields.amount.string = _t(this.state.data.str_has_amount);
                } else if (sdata === 'has_date') {
                    seq = this.state.data.number_has_date;
                    this.state.fields.date.string = _t(this.state.data.str_has_date);
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_date);
                    }
                } else if (sdata === 'has_location') {
                    seq = this.state.data.number_has_location;
                    this.state.fields.location.string = _t(this.state.data.str_has_location);
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_location);
                    }
                } else if (sdata === 'has_partner') {
                    seq = this.state.data.number_has_partner;
                    this.state.fields.partner_id.string = _t(this.state.data.str_has_partner);
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_partner);
                    }
                } else if (sdata === 'has_payment_method') {
                    seq = this.state.data.number_has_payment_method;
                } else if (sdata === 'has_period') {
                    seq = this.state.data.number_has_period;
                    node.attrs.string = _t(this.state.data.str_has_period);
                    this.state.fields.date_start.string = _t(this.state.data.str_has_period);
                } else if (sdata === 'has_product') {

                    seq = this.state.data.number_has_product;
                    this.state.fields.product_line_ids.string = _t(this.state.data.str_has_product);
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_product);
                    }
                } else if (sdata === 'has_quantity') {
                    seq = this.state.data.number_has_quantity;
                    this.state.fields.quantity.string = _t(this.state.data.str_has_quantity);
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_quantity);
                    }

                } else if (sdata === 'has_reference') {
                    seq = this.state.data.number_has_reference;
                    this.state.fields.reference.string = _t(this.state.data.str_has_reference);
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_reference);
                    }
                } else if (sdata === 'has_totalamount') {
                    seq = this.state.data.number_has_totalamount;
                    this.state.fields.totalamount.string = _t(this.state.data.str_has_totalamount);
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_totalamount);
                    }
                } else if (sdata === 'has_purpose') {
                    seq = this.state.data.number_has_purpose;
                    this.state.fields.purpose.string = _t(this.state.data.str_has_purpose);
                    if (node.attrs.string)
                    {
                        node.attrs.string = _t(this.state.data.str_has_purpose);
                    }
                }
            }

        }
        return seq;
    },

    _renderTagNotebook: function (node) {

        var len = node.children.length;
        for (var i = 0 ; i < len; i++)
        {
            var nseq =  this.getSeqnumberFromStateData(node.children[i]);
        }

        return this._super.apply(this, arguments);
    },
    _renderInnerGroup: function (node) {

        var numdata = this.state.data;


        if (this.state.model === "kapprove.doc")
        {

            if(node.tag === "group")
            {
                if(node.attrs.name === "request_main" || node.attrs.name === "request_details")
                {
                    var len = node.children.length;

                    for (var i = 0 ; i < len; i++)
                    {
                        var nseq =  this.getSeqnumberFromStateData(node.children[i])
                        var target = Object.assign(node.children[i], {seq:nseq});
                    }

                    if(node.children.length > 0)
                    {
                        node.children.sort(function(a, b){return a.seq - b.seq;});
                    }
                }
            }else if(node.tag === "notebook")
            {
                var len = node.children.length;

                for (var i = 0 ; i < len; i++)
                {
                    if(node.children[i].tag === "page")
                    {
                        console.log('---page----')
                        this.getSeqnumberFromStateData(node.children[i]);
                    }

                }
            }
        }
        return this._super.apply(this, arguments);
    },
    _updateView: function ($newContent) {

       var ret =  this._super.apply(this, arguments);
       if (this.state.model === "kapprove.doc") {
            setTimeout(function(){
               $("button.o_form_button_create").hide();
            } , 100);
            if(this.state.data.state !== "draft")
            {
               setTimeout(function(){
                   $("button.o_form_button_edit").hide();
               } , 100);
            }

       }
       return ret;
    }

});

});
