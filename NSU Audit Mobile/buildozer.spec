[app]

title = NSU Audit Core
package.name = nsuauditcore
package.domain = org.nsu

version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy>=2.3.0,reportlab,Pillow

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.3.0

fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.archs = arm64-v8a,armeabi-v7a

android.meta_data = com.google.android.gms.version.@integer/google_play_services_version

android.api = 33
android.minapi = 21
android.ndk_api = 25

presplash_filename = presplash.png
icon.filename = icon.png

[buildozer]

log_level = 2

warn_on_root = 1

build_dir = ./.buildozer

bin_dir = ./bin
