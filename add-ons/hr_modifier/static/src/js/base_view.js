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

odoo.define('hr_modifier.ListView', function (require) {
    'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb;
    
    ajax.loadXML('/hr_modifier/static/src/xml/button_add.xml', qweb);
});