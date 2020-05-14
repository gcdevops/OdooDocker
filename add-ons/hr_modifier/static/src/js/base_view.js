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
    var qweb = core.qweb
    ajax.loadXML('/hr_modifier/static/src/xml/button_add.xml', qweb);
});

odoo.define('hr_modifier.FilterMenuGenerator', function (require) {
    'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb
    ajax.loadXML('/hr_modifier/static/src/xml/custom_filter_add.xml', qweb);
})

odoo.define('hr_modifier.GroupByMenuGenerator', function (require) {
    'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb
    ajax.loadXML('/hr_modifier/static/src/xml/custom_group_add.xml', qweb);
})

odoo.define('hr_modifier.UserMenu', function (require) {
    'use strict';

    var UserMenu = require('web.UserMenu');

    UserMenu.include({

        start: function () {
            var self = this;
            var config = require('web.config');
            var session = require('web.session');

            this.$el.on('click', '[data-menu]', function (ev) {
                ev.preventDefault();
                var menu = $(this).data('menu');
                self['_onMenu' + menu.charAt(0).toUpperCase() + menu.slice(1)]();
            });
            return this._super.apply(this, arguments).then(function () {
                var $avatar = self.$('.oe_topbar_avatar');
                if (!session.uid) {
                    $avatar.attr('src', $avatar.data('default-src'));
                    return Promise.resolve();
                }
                var topbar_name = session.name;
                if (config.isDebug()) {
                    topbar_name = _.str.sprintf("%s (%s)", topbar_name, session.db);
                }

                session.user_has_group('hr_modifier.group_hr_senior_management').then(function(value) {
                    if (value == 1) {
                        topbar_name = _.str.sprintf("%s (%s)", topbar_name, "Senior Management");
                        self.$('.oe_topbar_name').text(topbar_name);
                    }
                });

                session.user_has_group('hr_modifier.group_hr_coordinator').then(function(value) {
                    if (value == 1) {
                        topbar_name = _.str.sprintf("%s (%s)", topbar_name, "Coordinator");
                        self.$('.oe_topbar_name').text(topbar_name);
                    }
                });

                session.user_has_group('hr_modifier.group_hr_reporter').then(function(value) {
                    if (value == 1) {
                        topbar_name = _.str.sprintf("%s (%s)", topbar_name, "Reporter");
                        self.$('.oe_topbar_name').text(topbar_name);
                    }
                });

                self.$('.oe_topbar_name').text(topbar_name);
                var avatar_src = session.url('/web/image', {
                    model:'res.users',
                    field: 'image_128',
                    id: session.uid,
                });
                $avatar.attr('src', avatar_src);
            });
        },
    });
});