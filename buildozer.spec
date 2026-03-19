[app]
title = OpenAgenda
package.name = openagenda
package.domain = org.openagenda
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
source.patterns = {'main': 'main.py'}

version = 1.4.0

requirements = python3,kivy==2.3.0,requests

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 34
android.minapi = 24
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
