odoo.define('k_approve_base.buttons', function (require) {
"use strict";

var ListController = require('web.ListController');
var ListView = require('web.ListView');
var viewRegistry = require('web.view_registry');

var TransactionsListController = ListController.extend({
    buttons_template: 'k_approve_base.buttons',

    events: _.extend({}, ListController.prototype.events, {
        'click .o_button_new_view': '_onOpenDocument',
    }),

    _onOpenDocument: function () {
        var self = this;
        self.do_action({
            type: 'ir.actions.act_window',
            name: 'Create Document',
            res_model: 'kapprove.doc.template',
            views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
            context: {"search_default_group_by_template": 1},
        });
    },
    _onOpenRecord: function (ev) {
        var selectedRecord = this.model.get(ev.data.id);
        var self = this;
        if (selectedRecord.model === "kapprove.doc.line" ) {
            var resid = selectedRecord.data.approve_doc_id.res_id
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Doc view',
                res_model: 'kapprove.doc',
                res_id: resid,
                views: [[false, 'form']],
            });
        }else {
            self.trigger_up('select_record', {
                id: selectedRecord.res_id,
                display_name: selectedRecord.data.display_name,
            });
        }
    },

});

var TransactionsListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: TransactionsListController,
    }),

});

viewRegistry.add('docopen_tree', TransactionsListView);
});