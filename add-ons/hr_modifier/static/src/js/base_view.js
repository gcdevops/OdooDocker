odoo.define('hr_modifier.BasicView', function (require) {
    "use strict";
    
    var BasicView = require('web.BasicView');
    BasicView.include({
        init: function(viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);
            self.controllerParams.archiveEnabled = 'False' in viewInfo.fields;            
        },
    });
});