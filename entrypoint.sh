#!/usr/bin/env bash
set -euo pipefail

cd /plugin
/usr/local/bin/octoprint dev plugin:install

/bin/bash /init
