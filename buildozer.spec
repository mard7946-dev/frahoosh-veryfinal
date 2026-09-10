[app]

title = Frahoosh
package.name = frahoosh
package.domain = org.frahoosh
source.dir = .
source.main = main.py
version = 1.0

requirements = python3==3.11.10,hostpython3==3.11.10,kivy==2.3.1,arabic-reshaper==3.0.0,python-bidi==0.6.6
orientation = portrait

icon.filename = %(source.dir)s/mobile/assets/frahoosh_logo.png
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,svg
source.include_patterns = mobile/*,mobile/**/*

android.archs = arm64-v8a
android.api = 35
android.minapi = 24
android.ndk = 28c
android.ndk_api = 24
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/28.2.13676358
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET
android.presplash_color = #000000
android.accept_sdk_license = True

p4a.fork = kivy
p4a.branch = v2026.05.09

fullscreen = 0
log_level = 2
