[app]

title = Frahoosh
package.name = frahoosh
package.domain = ir.frahoosh

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,ttf,otf,ico,svg

source.exclude_exts = spec

source.exclude_dirs = bin,.buildozer,.git,__pycache__,tests


version = 1.1.1
android.numeric_version = 2


requirements = python3==3.11.10,kivy==2.3.1,arabic-reshaper==3.0.0,python-bidi==0.6.6


orientation = portrait

fullscreen = 0


android.api = 35
android.minapi = 24

android.ndk = 28c
android.ndk_api = 24


android.archs = arm64-v8a


android.private_storage = True


android.skip_update = True

android.accept_sdk_license = True


android.permissions = INTERNET,ACCESS_NETWORK_STATE


android.enable_androidx = True


android.entrypoint = org.kivy.android.PythonActivity


p4a.bootstrap = sdl2

p4a.fork = kivy
p4a.branch = v2026.05.09



[buildozer]

log_level = 2

warn_on_root = 1
