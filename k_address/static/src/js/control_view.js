odoo.define('kaddress_Controller', function (require) {
    "use strict";

    var AbstractController = require('web.AbstractController');
    var core = require('web.core');
    // var Rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;


    var FormController = AbstractController.include({

        custom_events: _.extend({}, AbstractController.prototype.custom_events, {
            kaddress_set: '_onKaddress_set',
        }),
        start: function () {
            var def = this._super.apply(this, arguments);
            console.log('--start-FormController')
        },
        _onKaddress_set: function (ev) {
            var self = this;
            var lang = ev.data.lang;
            console.log('--_onKaddress_set')
            console.log(ev)
            this._rpc({
                route: '/web/view/edit_sido_address',
                params: {
                    sido: ev.data.data.sido,  //sidoEnglish
                    lang: ev.data.lang,  //sidoEnglish
                }
            }).then(function (result) {

                var country_id = 0;
                var state_id = 0;
                var country_name = "";
                var state_name = "";
                var user_country_code = "";

                if(result)
                {
                    country_id = result.country_id;
                    country_name = result.country_name;
                    state_id = result.state_id;
                    state_name = result.state_name;
                    user_country_code = result.user_country_code;
                    console.log('----country code' + user_country_code)
                }

                var sido = ""
                var address = ""
                var sigungu = ""
                var roadname = ""
                var sido_eng = ""
                var address_eng = ""
                var sigungu_eng = ""
                var roadname_eng = ""


                sido = ev.data.data.sido;
                address = ev.data.data.address;
                sigungu = ev.data.data.sigungu;
                roadname = ev.data.data.roadname;

                sido_eng = ev.data.data.sidoEnglish;
                address_eng = ev.data.data.addressEnglish;
                sigungu_eng = ev.data.data.sigunguEnglish;
                roadname_eng = ev.data.data.roadnameEnglish;

                if(lang !== 'ko_KR')
                {
                    address = ev.data.data.addressEnglish;
                    address_eng = ev.data.data.address;
                }

                var k_address1 = self.renderer.idsForLabels.k_address1;
                var smodal = '.modal-dialog'
                var modal = $(smodal);
                console.log(modal);
                var sel = "#" + k_address1;
                if (modal.length > 0)
                {
                    sel = smodal + " #" + k_address1;
                }

                var selector = $(sel);
                console.log(selector);
                selector.val(address);
                selector.trigger("change");

                var k_address1_eng = self.renderer.idsForLabels.k_address1_eng;
                sel = "#" + k_address1_eng;
                if (modal.length > 0)
                {
                    sel = smodal + " #" + k_address1_eng;
                }
                selector = $(sel);
                console.log(selector);
                selector.val(address_eng);
                selector.trigger("change");

                var k_zip = self.renderer.idsForLabels.zip;
                sel = "#" + k_zip
                if (modal.length > 0)
                {
                    sel = smodal + " #" + k_zip;
                }

                var zip = ev.data.data.zonecode;
                selector = $(sel)
                selector.val(zip);
                selector.trigger("change");
                console.log(self.renderer.idsForLabels)

                var city = self.renderer.idsForLabels.city;
                sel = "#" + city;
                if (modal.length > 0)
                {
                    sel = smodal + " #" + city;
                }

                selector = $(sel)
                selector.val(sigungu);
                selector.trigger("change");


                var street = self.renderer.idsForLabels.street;
                sel = "#" + street;
                if (modal.length > 0)
                {
                    sel = smodal + " #" + street;
                }
                selector = $(sel)
                selector.val(roadname);
                selector.trigger("change");


                var sid = self.renderer.idsForLabels.country_id;
                console.log(sid)
                sel = "#" + sid;
                if (modal.length > 0)
                {
                    sel = smodal + " #" + sid;
                }
                var ssid = country_name;
                selector = $(sel);
                selector.val(ssid);
                selector.data( "value_id", country_id );
                selector.data( "value_name", country_name );
                var e = $.Event('inputcomplete');
                selector.trigger(e);

                sid = self.renderer.idsForLabels.state_id;
                console.log(sid)
                sel = "#" + sid;
                if (modal.length > 0)
                {
                    sel = smodal + " #" + sid;
                }
                ssid = country_name;
                selector = $(sel);
                selector.val(ssid);
                selector.data( "value_id", state_id );
                selector.data( "value_name", state_name );
                var e = $.Event('inputcomplete');
                selector.trigger(e);


            });
        }
    });
    return FormController;
});