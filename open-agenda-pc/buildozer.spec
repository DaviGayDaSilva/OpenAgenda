[app]
title = OpenAgenda
package.name = openagenda
package.domain = org.openagenda
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.4.0

requirements = python3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 34
android.minapi = 21
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
