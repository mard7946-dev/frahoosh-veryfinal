# Frahoosh Mobile — Project Status

## Current foundation (v1.1.2)
- Cleaned all Python syntax errors in the current repository.
- Added a real loading screen before Login/Dashboard.
- Added bundled Persian/Arabic Noto font (regular/bold).
- Added RTL text shaping support.
- Fixed session storage to use Android app-private storage when running on device.
- Kept Supabase Auth as the login backend; no service_role key is used in the client.
- Improved profile/role extraction from Supabase user metadata and account_settings.
- Added role-specific dashboard module menus for the supported Frahoosh roles.
- Added a real module navigation screen instead of routing every dashboard button to Update.
- Added packaged runtime configuration support for CI builds without committing credentials.
- Added explicit Python dependency versions.

## Important
The role dashboards and module navigation are now structurally ready, but each module's CRUD/data operations must be connected to the exact Web v16.12 Supabase schema and RLS policies. No fake tables or invented schema are used here.

## CI configuration
Set these GitHub repository Secrets/Variables before expecting online login inside the APK:
- Secret: `FRAHOOSH_SUPABASE_URL`
- Secret: `FRAHOOSH_SUPABASE_ANON_KEY`
- Variable: `FRAHOOSH_SCHOOL_ID`
- Variable: `FRAHOOSH_SCHOOL_NAME`
- Variable: `FRAHOOSH_SCHOOL_YEAR`


## Android CI fix — 2026-08-31
The Android workflow was corrected so SDK package installation does not use `yes | sdkmanager ...` under `set -o pipefail`. That pattern causes a false `Broken pipe` exit code after sdkmanager finishes normally. The workflow now installs SDK packages directly, installs NDK 28c explicitly, generates `mobile/runtime_config.json` from GitHub Secrets/Variables, and runs `python -m compileall -q mobile` before Buildozer.


## Android CI fix — 2026-09-09
The failed build was traced to the Python-for-Android dependency stage, not the Kivy performance hints.
The workflow was allowing p4a to select Python 3.14.2 and then its pip fallback selected a
`charset-normalizer` Android wheel that pip rejected as unsupported. The app does not import
`requests` (it uses urllib directly), so `requests` and its problematic dependency chain were
removed from the mobile build requirements. The Android recipe is now pinned to Python 3.11.10
for reproducible builds, and CI generates `mobile/runtime_config.json` from GitHub Secrets/Variables.

## Panel status
All current dashboard routes now have a real screen destination and no longer depend on the old
Update placeholder. However, this repository does NOT contain the Web v16.12 database schema/RLS
definition, so CRUD against unknown tables is deliberately not fabricated. The only server table
currently proven by this codebase is `account_settings`. Exact CRUD wiring for students, teachers,
parents, finance, online classes, smart board and AI requires the authoritative Web v16.12 schema.
