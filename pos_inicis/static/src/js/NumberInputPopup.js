odoo.define('pos_inicis.NumberInputPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _lt } = require('@web/core/l10n/translation');

    const { onMounted, useRef, useState } = owl;

    // formerly NumberInputPopupWidget
    class NumberInputPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.state = useState({ inputValue: this.props.startingValue });
            this.inputRef = useRef('input');
            onMounted(this.onMounted);
        }
        onMounted() {
            this.inputRef.el.focus();
        }
        getPayload() {
            return this.state.inputValue;
        }
    }
    NumberInputPopup.template = 'NumberInputPopup';
    NumberInputPopup.defaultProps = {
        confirmText: _lt('Ok'),
        cancelText: _lt('Cancel'),
        title: '',
        body: '',
        startingValue: '',
        placeholder: '',
    };

    Registries.Component.add(NumberInputPopup);

    return NumberInputPopup;
});
