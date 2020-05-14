
odoo.define('hr_modifier.ListView', function (require) {
    'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb
    
    ajax.loadXML('/hr_modifier/static/src/xml/button_add.xml', qweb);
});