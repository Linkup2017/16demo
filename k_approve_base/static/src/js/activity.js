odoo.define('my.component1', function (require) {
    "use strict";

    const { Component, useState } = owl;
    const { xml } = owl.tags;
    const { patch } = require('web.utils');
    const MyComponent = require("my.component");
    console.log(MyComponent)

    patch(MyComponent.prototype, "test_patching_my_component", {
        setup() {
            this._super(...arguments);
            console.log("patch patch patch setup");
        },
        onNext(ev) {
            this.state.currentIndex++;
             console.log("patch onNext---");
        }
    });

    owl.utils.whenReady().then(() => {
        const app = new MyKComponent();
        app.mount(document.body);
    });

});