odoo.define('hr_modifier.AbstractWebClient', function (require) {
    "use strict";

    var AbstractWebClient = require('web.AbstractWebClient');

    AbstractWebClient.include({

        init: function (parent) {
            this._super(parent);
            this.set('title_part', {"zopenerp": "Listeblanche RH | HR Whitelist"});
        },

    });
});