odoo.define("kaddress.render_form", function (require) {
    "use strict";

    const FormRenderer = require('web.FormRenderer');
    console.log('--kaddress.render_form---')

    FormRenderer.include({
        events: _.extend({}, FormRenderer.prototype.events, {
            'click .o_korea_address_find': '_onKoreaAddressFind',
        }),
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            console.log('--FormRenderer init---')
        },
        updateState: function () {
            console.log('--updateState---')
            return this._super(...arguments);
        },
        _onKoreaAddressFind: function (ev) {
            var self = this;
            ev.stopPropagation();
            console.log('--FormRenderer---')
            console.log(self)
            var themeObj = {
               searchBgColor: "#0B65C8", //검색창 배경색
               queryTextColor: "#FFFFFF" //검색창 글자색
            };

            new daum.Postcode({
                theme: themeObj,
                oncomplete: function(data) {
                    var context = {};
                    context['data']  = data;
                    context['lang'] = self.state.context.lang; //en_US . ko_KR
                    console.log('--lang:' + self.state.context.lang)

                    console.log(self)
                    self.trigger_up('kaddress_set', context);
                }
            }).open({
                popupName: '주소 검색' , //팝업 이름을 설정(영문,한글,숫자 모두 가능, 영문 추천)
                q:''
            });

        },
        disableButtons: function () {
            console.log('---disableButtons---')
            const allButtons = this.$el[0].querySelectorAll('.o_statusbar_buttons button, .oe_button_box button');
            for (const button of allButtons) {
                if (!button.getAttribute("disabled")) {
                    // this.manuallyDisabledButtons.add(button)
                    // button.setAttribute("disabled", true)
                }
            }
        },
    });

});