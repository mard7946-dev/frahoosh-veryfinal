[app]

title = Frahoosh
package.name = frahoosh
package.domain = org.frahoosh
source.dir = .
source.main = main.py
version = 1.0

# Keep the proven dependency strategy from the previously green build.
# Do not pin packages that python-for-android also resolves internally.
requirements = python3,kivy,requests,urllib3,arabic-reshaper,python-bidi
orientation = portrait

icon.filename = %(source.dir)s/mobile/assets/frahoosh_logo.png
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,svg
source.include_patterns = mobile/*,mobile/**/*

android.archs = arm64-v8a
android.api = 35
android.minapi = 23
android.ndk = 28c
android.ndk_api = 23
android.entrypoint = org.kivy.android.PythonActivity
android.permissions = INTERNET
android.presplash_color = #000000
android.accept_sdk_license = True

fullscreen = 0
log_level = 2
