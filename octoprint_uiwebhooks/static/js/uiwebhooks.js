/*
 * View model for OctoPrint-UIWebhooks
 *
 * Author: PaddyCo
 * License: AGPLv3
 */
$(function() {
    function UiwebhooksViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        self.onTrigger = function(t) {
            OctoPrint.simpleApiCommand("uiwebhooks", "trigger", { webhook_id: t.webhook_id() })
        }

        self.onHashChange = function(t) {
            var hash = t.value().indexOf("#") == 0 ? t.value() : "#" + t.value();

            if (hash == window.location.hash) {
                self.onTrigger(t);
            }

            $(window).on('hashchange', function(e) {
                if (hash == window.location.hash) {
                    self.onTrigger(t);
                }
            });
        }

        self.bindTrigger = function(t) {
            switch (t.kind()) {
                case "HashChange":
                    self.onHashChange(t);
                    break;
                default:
                    console.warn("UI Webhooks: Unknown trigger type '" + t.kind() + "' assigned, skipping.");
                    return;

            }
        }

        self.onBeforeBinding = function() {
            var settings = self.settingsViewModel.settings.plugins.uiwebhooks;
            var triggers = settings.triggers();

            triggers.forEach(self.bindTrigger);
        }
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: UiwebhooksViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_uiwebhooks, #tab_plugin_uiwebhooks, ...
        elements: [ /* ... */ ]
    });
});
