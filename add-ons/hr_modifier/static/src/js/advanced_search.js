
odoo.define('hr_modifier.advanced_search_button', function (require) {
  "use strict";
  var core = require('web.core');

  var ListController = require('web.ListController');
  ListController.include({
    renderButtons: function ($node) {
      this._super.apply(this, arguments);
      if (this.$buttons) {
        let search_button = this.$buttons.find('.oe_advanced_search_button');
        search_button && search_button.click(this.proxy('search_button'));
      }
    },
    search_button: function () {
      var self = this;
      var action = {
        type: "ir.actions.act_window",
        name: "Advanced Search",
        res_model: "hr.employee",
        views: [[false, "form"]],
        target: "new",
        view_type: "form",
        view_mode: "form",
        flags: { "form": { "action_buttons": true, "options": { "mode": "edit" } } }
      };
      return this.do_action(action);
    }
  });
});

var AbstractController = require('web.AbstractController');
var AbstractModel = require('web.AbstractModel');
var AbstractRenderer = require('web.AbstractRenderer');
var AbstractView = require('web.AbstractView');

var MapController = AbstractController.extend({});
var MapRenderer = AbstractRenderer.extend({});
var MapModel = AbstractModel.extend({});

var MapView = AbstractView.extend({
    config: {
        Model: MapModel,
        Controller: MapController,
        Renderer: MapRenderer,
    },
});
var viewRegistry = require('web.view_registry');

viewRegistry.add('map', MapView);
