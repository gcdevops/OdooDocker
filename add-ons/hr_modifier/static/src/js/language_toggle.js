
odoo.define("hr_modifier.LanguageToggle",function(require){
    "use strict";

    var Widget = require("web.Widget");
    var SystrayMenu = require('web.SystrayMenu');
    var session = require("web.session")
    var rpc = require("web.rpc")

    var LanguageToggle = Widget.extend({
        template:"hr_modifier.languageToggle",
        events: {
            "click button": "_onClick"
        },
        _onClick: function () {
            
            var lang_to_switch_to = ""
            if (this.active_language === "English"){
                if (this.active_languages.includes("fr_CA")){
                    lang_to_switch_to = "fr_CA"
                }
                else{
                    lang_to_switch_to = "fr_FR"
                }
            }

            else{
                if( this.active_languages.includes("en_CA")){
                    lang_to_switch_to = "en_CA"
                }
                else{
                    lang_to_switch_to = "en_US"
                }
            }

            return rpc.query({
                model: "res.users",
                method: "write",
                args: [
                    session.uid,
                    {
                        lang: lang_to_switch_to
                    }
                ]
            }).then(
                function(result){
                    window.location.reload()
                }
            )
        },

        willStart: function (){
            var self = this
            return rpc.query(
                {
                    model: "res.lang",
                    method: "search_read",
                    args: [[["active", "=", true]]]
                }
            ).then(function(result){
                self.active_languages = result.map(function(item){
                    return item.code
                })

                if(! self.active_languages.includes("en_US") && ! self.active_languages.includes("en_CA")){
                    self.active = false
                }
                else if ( ! self.active_languages.includes("fr_CA") && ! self.active_languages.includes("fr_FR")){
                    self.active = false
                }
                else{
                    self.active = true 
                }
            })
        },
        start:function(){
            if (this.active){
                var currentLanguage = session.user_context["lang"]
                var switchToLanguage = ""

                if (currentLanguage === "en_US" || currentLanguage === "en_CA"){
                    switchToLanguage = "Français"
                    this.active_language = "English"
                }

                if (currentLanguage === "fr_FR" || currentLanguage === "fr_CA"){
                    switchToLanguage = "English"
                    this.active_language = "French"
                }
                this.$el.children("button").text(switchToLanguage)
                this.$el.css("display", "flex")
            }
            else{
                this.$el.hide()
            }
        }
    });
    LanguageToggle.prototype.sequence = -10000;
    SystrayMenu.Items.push(LanguageToggle);
    return LanguageToggle
})
