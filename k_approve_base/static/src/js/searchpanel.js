/** @odoo-module **/

import SearchPanel from "web.searchPanel";
const { patch, unpatch } = require('web.utils');

patch(SearchPanel.prototype, 'k_approve_base.SearchPanel', {
      mounted() {
            this._updateGroupHeadersChecked();
            if (this.hasImportedState) {
                this.el.scroll({ top: this.scrollTop });
            }
            var sections = this.model.get("sections", s => !s.empty);
            console.log('-----mounted')
            console.log(sections)
            console.log(this.model)
            if(sections.length > 0 && this.model.config.modelName === 'kapprove.doc.line')
            {
                this.model.dispatch("toggleCategoryValue", sections[0].id, false);
                this.model.dispatch("toggleCategoryValue", sections[1].id, false);
                this.model.dispatch("toggleCategoryValue", sections[2].id, false);

            }
      }

});


