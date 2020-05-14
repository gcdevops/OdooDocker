
odoo.define('hr_modifier.UserMenu', function (require) {
  'use strict';

  var core = require('web.core');
  var ajax = require('web.ajax');
  var qweb = core.qweb
  
  ajax.loadXML('/hr_modifier/static/src/xml/user_menu.xml', qweb);
});