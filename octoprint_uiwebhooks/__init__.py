# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.access.permissions as permissions
import flask
import requests

class UiwebhooksPlugin(
        octoprint.plugin.SettingsPlugin,
        octoprint.plugin.AssetPlugin,
        octoprint.plugin.SimpleApiPlugin,
        octoprint.plugin.TemplatePlugin
):

    ##
    # SettingsPlugin mixin
    ##
    def get_settings_defaults(self):
        return {
            "triggers": [],
            "webhooks": {}
        }

    def get_settings_restricted_paths(self):
        return {
            permissions.Permissions.SETTINGS_READ: [["triggers"],],
            permissions.Permissions.SETTINGS: [["webhooks"],],
        }

    ##
    # AssetPlugin mixin
    ##
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/uiwebhooks.js"],
            "css": ["css/uiwebhooks.css"],
            "less": ["less/uiwebhooks.less"]
        }

    ##
    # SimpleAPIPlugin mixin
    ##
    def get_api_commands(self):
        return dict(
            trigger=["webhook_id"],
        )

    def on_api_command(self, command, data):
        import flask
        with permissions.Permissions.SETTINGS_READ.require(http_exception=403):
            if command == "trigger":
                self._logger.info("Trigger called for webhook {webhook_id}".format(**data))
                webhook_url = self._settings.get(["webhooks"])[data["webhook_id"]]
                requests.post(webhook_url)

    ###
    # Softwareupdate hook
    ###
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "uiwebhooks": {
                "displayName": "Uiwebhooks Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "PaddyCo",
                "repo": "OctoPrint-UIWebhooks",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/PaddyCo/OctoPrint-UIWebhooks/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "UI Webhooks"
__plugin_pythoncompat__ = ">=3,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = UiwebhooksPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
