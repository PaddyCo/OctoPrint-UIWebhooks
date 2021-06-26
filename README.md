# OctoPrint-UIWebhooks

Adds ways to trigger webhooks by various actions performed in the UI

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/PaddyCo/OctoPrint-UIWebhooks/archive/main.zip

## Configuration

### Trigger types

* `HashChange`, value is the hash you want the trigger to look for

### Example

Turn on the lights automatically when someone views the #control tab (which contains the webcam feed) by pushing to a HomeAssistant webhook:

``` yaml
plugins:
  uiwebhooks:
    triggers:
      - kind: HashChange
        value: control
        webhook_id: turn_on_lights
    webhooks:
      turn_on_lights: https://homeassistant.local:8123/api/webhook/octoprint_webcam_accessed
```
