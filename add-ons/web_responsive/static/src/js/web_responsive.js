/* Copyright 2018 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

 odoo.define("web_responsive", function(require) {
    "use strict";

    const ActionManager = require("web.ActionManager");
    const AbstractWebClient = require("web.AbstractWebClient");
    const BasicController = require("web.BasicController");
    const config = require("web.config");
    const core = require("web.core");
    const FormRenderer = require("web.FormRenderer");
    const Menu = require("web.Menu");
    const RelationalFields = require("web.relational_fields");
    const Chatter = require("mail.Chatter");
    const ListRenderer = require("web.ListRenderer");
    const DocumentViewer = require("mail.DocumentViewer");

    /**
     * Reduce menu data to a searchable format understandable by fuzzy.js
     *
     * `AppsMenu.init()` gets `menuData` in a format similar to this (only
     * relevant data is shown):
     *
     * ```js
     * {
     *  [...],
     *  children: [
     *    // This is a menu entry:
     *    {
     *      action: "ir.actions.client,94", // Or `false`
     *      children: [... similar to above "children" key],
     *      name: "Actions",
     *      parent_id: [146, "Settings/Technical/Actions"], // Or `false`
     *    },
     *    ...
     *  ]
     * }
     * ```
     *
     * This format is very hard to process to search matches, and it would
     * slow down the search algorithm, so we reduce it with this method to be
     * able to later implement a simpler search.
     *
     * @param {Object} memo
     * Reference to current result object, passed on recursive calls.
     *
     * @param {Object} menu
     * A menu entry, as described above.
     *
     * @returns {Object}
     * Reduced object, without entries that have no action, and with a
     * format like this:
     *
     * ```js
     * {
     *  "Discuss": {Menu entry Object},
     *  "Settings": {Menu entry Object},
     *  "Settings/Technical/Actions/Actions": {Menu entry Object},
     *  ...
     * }
     * ```
     */
    function findNames(memo, menu) {
        if (menu.action) {
            var key = menu.parent_id ? menu.parent_id[1] + "/" : "";
            memo[key + menu.name] = menu;
        }
        if (menu.children.length) {
            _.reduce(menu.children, findNames, memo);
        }
        return memo;
    }

    Menu.include({
        events: _.extend(
            {
                // Clicking a hamburger menu item should close the hamburger
                "click .o_menu_sections [role=menuitem]": "_onClickMenuItem",
                // Opening any dropdown in the navbar should hide the hamburger
                "show.bs.dropdown .o_menu_systray, .o_menu_apps": "_hideMobileSubmenus",
            },
            Menu.prototype.events
        ),

        start: function() {
            this.$menu_toggle = this.$(".o-menu-toggle");
            return this._super.apply(this, arguments);
        },

        /**
         * Hide menus for current app if you're in mobile
         */
        _hideMobileSubmenus: function() {
            if (
                config.device.isMobile &&
                this.$menu_toggle.is(":visible") &&
                this.$section_placeholder.is(":visible")
            ) {
                this.$section_placeholder.collapse("hide");
            }
        },

        /**
         * Prevent hide the menu (should be closed when action is loaded)
         *
         * @param {ClickEvent} ev
         */
        _onClickMenuItem: function(ev) {
            ev.stopPropagation();
        },

        /**
         * No menu brand in mobiles
         *
         * @override
         */
        _updateMenuBrand: function() {
            if (!config.device.isMobile) {
                return this._super.apply(this, arguments);
            }
        },
    });

    RelationalFields.FieldStatus.include({
        /**
         * Fold all on mobiles.
         *
         * @override
         */
        _setState: function() {
            this._super.apply(this, arguments);
            if (config.device.isMobile) {
                _.map(this.status_information, value => {
                    value.fold = true;
                });
            }
        },
    });

    // Sticky Column Selector
    ListRenderer.include({
        _renderView: function() {
            const self = this;
            return this._super.apply(this, arguments).then(() => {
                const $col_selector = self.$el.find(
                    ".o_optional_columns_dropdown_toggle"
                );
                if ($col_selector.length !== 0) {
                    const $th = self.$el.find("thead>tr:first>th:last");
                    $col_selector.appendTo($th);
                }
            });
        },

        _onToggleOptionalColumnDropdown: function(ev) {
            // FIXME: For some strange reason the 'stopPropagation' call
            // in the main method don't work. Invoking here the same method
            // does the expected behavior... O_O!
            // This prevents the action of sorting the column from being
            // launched.
            ev.stopPropagation();
            this._super.apply(this, arguments);
        },
    });

    // Responsive view "action" buttons
    FormRenderer.include({
        /**
         * In mobiles, put all statusbar buttons in a dropdown.
         *
         * @override
         */
        _renderHeaderButtons: function() {
            const $buttons = this._super.apply(this, arguments);
            if (
                !config.device.isMobile ||
                !$buttons.is(":has(>:not(.o_invisible_modifier))")
            ) {
                return $buttons;
            }

            // $buttons must be appended by JS because all events are bound
            $buttons.addClass("dropdown-menu");
            const $dropdown = $(
                core.qweb.render("web_responsive.MenuStatusbarButtons")
            );
            $buttons.addClass("dropdown-menu").appendTo($dropdown);
            return $dropdown;
        },
    });

    // Chatter Hide Composer
    Chatter.include({
        _openComposer: function(options) {
            if (
                this._composer &&
                options.isLog === this._composer.options.isLog &&
                this._composer.$el.is(":visible")
            ) {
                this._closeComposer(false);
            } else {
                this._super.apply(this, arguments);
            }
        },
    });

    /**
     * Use ALT+SHIFT instead of ALT as hotkey triggerer.
     *
     * HACK https://github.com/odoo/odoo/issues/30068 - See it to know why.
     *
     * Cannot patch in `KeyboardNavigationMixin` directly because it's a mixin,
     * not a `Class`, and altering a mixin's `prototype` doesn't alter it where
     * it has already been used.
     *
     * Instead, we provide an additional mixin to be used wherever you need to
     * enable this behavior.
     */
    var KeyboardNavigationShiftAltMixin = {
        /**
         * Alter the key event to require pressing Shift.
         *
         * This will produce a mocked event object where it will seem that
         * `Alt` is not pressed if `Shift` is not pressed.
         *
         * The reason for this is that original upstream code, found in
         * `KeyboardNavigationMixin` is very hardcoded against the `Alt` key,
         * so it is more maintainable to mock its input than to rewrite it
         * completely.
         *
         * @param {keyEvent} keyEvent
         * Original event object
         *
         * @returns {keyEvent}
         * Altered event object
         */
        _shiftPressed: function(keyEvent) {
            const alt = keyEvent.altKey || keyEvent.key === "Alt",
                newEvent = _.extend({}, keyEvent),
                shift = keyEvent.shiftKey || keyEvent.key === "Shift";
            // Mock event to make it seem like Alt is not pressed
            if (alt && !shift) {
                newEvent.altKey = false;
                if (newEvent.key === "Alt") {
                    newEvent.key = "Shift";
                }
            }
            return newEvent;
        },

        _onKeyDown: function(keyDownEvent) {
            return this._super(this._shiftPressed(keyDownEvent));
        },

        _onKeyUp: function(keyUpEvent) {
            return this._super(this._shiftPressed(keyUpEvent));
        },
    };

    // Include the SHIFT+ALT mixin wherever
    // `KeyboardNavigationMixin` is used upstream
    AbstractWebClient.include(KeyboardNavigationShiftAltMixin);

    // DocumentViewer: Add support to maximize/minimize
    DocumentViewer.include({
        // Widget 'keydown' and 'keyup' events are only dispatched when
        // this.$el is active, but now the modal have buttons that can obtain
        // the focus. For this reason we now listen core events, that are
        // dispatched every time.
        events: _.extend(
            _.omit(DocumentViewer.prototype.events, ["keydown", "keyup"]),
            {
                "click .o_maximize_btn": "_onClickMaximize",
                "click .o_minimize_btn": "_onClickMinimize",
                "shown.bs.modal": "_onShownModal",
            }
        ),

        start: function() {
            core.bus.on("keydown", this, this._onKeydown);
            core.bus.on("keyup", this, this._onKeyUp);
            return this._super.apply(this, arguments);
        },

        destroy: function() {
            core.bus.off("keydown", this, this._onKeydown);
            core.bus.off("keyup", this, this._onKeyUp);
            this._super.apply(this, arguments);
        },

        _onShownModal: function() {
            // Disable auto-focus to allow to use controls in edit mode.
            // This only affects the active modal.
            // More info: https://stackoverflow.com/a/14795256
            $(document).off("focusin.modal");
        },
        _onClickMaximize: function() {
            this.$el.removeClass("o_responsive_document_viewer");
        },
        _onClickMinimize: function() {
            this.$el.addClass("o_responsive_document_viewer");
        },
    });
});
