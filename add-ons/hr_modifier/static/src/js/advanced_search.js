
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
        views: [[false, "advanced_search"]],
        target: "new",
        //view_type: "advanced_search",
        //view_mode: "advanced_search",
        flags: { "advanced_search": { "action_buttons": true, "options": { "mode": "edit" } } }
      };
      return this.do_action(action);
    }
  });
});

odoo.define('hr.advanced_search', function(require){
  "use strict";
  
  var AbstractController = require('web.AbstractController');
  var AbstractModel = require('web.AbstractModel');
  var AbstractRenderer = require('web.AbstractRenderer');
  var AbstractView = require('web.AbstractView');
  
  var AdvancedSearchController = AbstractController.extend({});
  var AdvancedSearchRenderer = AbstractRenderer.extend({});
  var AdvancedSearchModel = AbstractModel.extend({});
  
  var AdvancedSearchView = AbstractView.extend({
      config: {
          Model: AdvancedSearchModel,
          Controller: AdvancedSearchController,
          Renderer: AdvancedSearchRenderer,
      },
  });
  var viewRegistry = require('web.view_registry');
  
  viewRegistry.add('advanced_search', AdvancedSearchView);
})

