odoo.define("hr_modifier.CustomTitle", function (require) {
  "use strict";

  var Widget = require("web.Widget");
  var SystrayMenu = require('web.SystrayMenu');
  var session = require("web.session")
  var dom = require("web.dom");
  var rpc = require("web.rpc")

  var CustomTitle = Widget.extend({
    willStart: function () {
      var self = this
      return rpc.query({
        model: "hr.employee",
        method: "search_read",
        args: [[["user_id", "=", session.uid]]]
      }).then(function (result) {
        if (result && result.length > 0 && result[0].x_department_coordinators_ids && result[0].x_department_coordinators_ids.length > 0) {

          var prefix = "";
          if (result[0].in_group_15){
            prefix = "Coordinator for ";
          }
          else if (result[0].in_group_16){
            prefix = "Reporter for ";
          }

          rpc.query({
            model: "hr.department",
            method: "search_read",
            args: [[["id", "in", result[0].x_department_coordinators_ids]]]
          }).then(function (result) {
            if (result && result.length > 0 && result[0].name) {
              var branchNames = []
              for (let i in result){
                branchNames.push(result[i].name)
              }

              dom.append($("header nav"), "<span class='o_team_name'>"+ prefix + branchNames.join(", ") + "</span>");
            }
            
          })
        }

      });
    }
  });
  CustomTitle.prototype.sequence = -20000;
  SystrayMenu.Items.push(CustomTitle);
  return CustomTitle
})