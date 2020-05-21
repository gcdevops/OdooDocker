odoo.define("hr_modifier.LanguageToggle",function(require){
  "use strict";
  var ControlPanelMixin = require('web.ControlPanelMixin');
  var Widget = require('web.Widget');

  var ClientAction = Widget.extend(ControlPanelMixin, {
    start: function() {
      this._renderButtons();
      this._updateControlPanel();
    },
    do_show: function() {
      this._updateControlPanel();
    },
    _renderButtons: function() {

    },
    _updateControlPanel: function() {
      this.update_control_panel({
        cp_content: {
          $buttons: this.buttons;
        }
      })
    }
  });

}