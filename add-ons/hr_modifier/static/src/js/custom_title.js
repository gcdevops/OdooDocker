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
        model: "res.users",
        method: "search_read",
        args: [[["id", "=", session.uid]]]
      }).then(function (result) {

        if (result && result.length > 0 && result[0].x_department_coordinators_ids && result[0].x_department_coordinators_ids.length > 0) {
          rpc.query({
            model: "hr.department",
            method: "search_read",
            args: [[["id", "in", result[0].x_department_coordinators_ids]]]
          }).then(function (result) {
            var showBranch = false;
            var branchName = "";

            const regex = /model=([^&]*)/g;
            var model = window.location.toString().match(regex)
            if (model && model.length > 0) {
              if (model[0].substr(6, model[0].length - 1) === "hr.employee") {
                showBranch = true;
              }
            }

            if (result && result.length > 0 && result[0].name) {
              branchName = result[0].name;
            }
            else {
              branchName = "";
            }

            if (showBranch) {
              dom.append($("header nav"), "<span class='o_team_name'>" + branchName + "</span>");
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