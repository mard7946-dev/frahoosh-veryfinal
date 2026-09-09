[app]

# (str) Title of your application

title = Frahoosh

# (str) Package name

package.name = frahoosh

# (str) Package domain

package.domain = org.frahoosh

# (str) Source code where main.py is located

source.dir = .

# (str) Main Python file

source.main = main.py

# (str) Application version

version = 1.0

# (list) Application requirements

requirements = python3==3.11.10,kivy==2.3.1,arabic-reshaper==3.0.0,python-bidi==0.6.6

# (str) Supported orientation

orientation = portrait

# (str) Presplash of the application

# presplash.filename = %(source.dir)s/mobile/assets/frahoosh_logo.png

# (str) Icon of the application

icon.filename = %(source.dir)s/mobile/assets/frahoosh_logo.png

# (str) Include these file extensions

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,svg

# (list) List of inclusions using pattern matching

source.include_patterns = mobile/*,mobile/**/*

# (str) Supported architectures

android.archs = arm64-v8a

# (int) Target Android API

android.api = 35

# (int) Minimum Android API

android.minapi = 24

# (str) Android NDK version

android.ndk = 28c

# (int) Android NDK API

android.ndk_api = 24

# (str) Python-for-Android fork

p4a.fork = kivy

# (str) Python-for-Android branch

p4a.branch = v2026.05.09

# (bool) Fullscreen

fullscreen = 0

# (str) Android application theme

android.entrypoint = org.kivy.android.PythonActivity

# (str) Android permissions

android.permissions = INTERNET

# (str) Android application name

android.presplash_color = #000000

# (bool) Don't update SDK automatically

android.skip_update = 0

# (str) Android accept SDK licenses

android.accept_sdk_license = True

# (str) Android build tools version

android.sdk_path =

# (str) Android NDK path

android.ndk_path =

# (str) Log level

log_level = 2

                    
