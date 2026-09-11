[app]

title = Frahoosh
package.name = frahoosh
package.domain = org.frahoosh
source.dir = .
source.main = main.py
version = 1.1.3

requirements = python3,kivy==2.3.1,arabic-reshaper==3.0.0,python-bidi==0.6.6
orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/mobile/assets/frahoosh_logo.png
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,svg
source.include_patterns = mobile/*,mobile/**/*

android.archs = arm64-v8a
android.api = 35
android.minapi = 23
android.ndk = 25c
android.ndk_api = 23
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET
android.presplash_color = #000000
android.accept_sdk_license = True

log_level = 2
