# Frahoosh Mobile — v1.1.0 Foundation Fixed

نسخه تمیز و اصلاح‌شده Mobile فراهوش بر پایه مخزن فعلی.

## تغییرات این نسخه
- رفع کامل SyntaxErrorهای موجود در `mobile/`.
- اضافه شدن Loading Screen واقعی قبل از Login.
- فونت فارسی/عربی Noto به‌صورت Bundled داخل APK.
- پشتیبانی RTL و شکل‌دهی متن فارسی.
- اصلاح محل ذخیره Session برای Android با استفاده از app-private storage.
- Login غیرمسدودکننده UI با Supabase Auth.
- استخراج Role/Profile از user metadata و `account_settings`.
- Dashboard نقش‌محور برای نقش‌های اصلی فراهوش.
- مسیر واقعی Dashboard → Module به جای اینکه همه دکمه‌ها به Update بروند.
- پشتیبانی Runtime Configuration در CI بدون Commit کردن کلید Supabase.
- نسخه‌های دقیق dependencyها برای reproducible build.

## اجرای محلی
```bash
python -m venv .venv
# activate the venv
pip install -r requirements.txt
python -m mobile.main
```

برای اجرای محلی، متغیرهای `.env.example` را در shell تنظیم کنید.

## GitHub Actions / Android
Workflow قبل از Build فایل `mobile/runtime_config.json` را از Secret/Variableهای GitHub می‌سازد.

### Secrets
- `FRAHOOSH_SUPABASE_URL`
- `FRAHOOSH_SUPABASE_ANON_KEY`

### Variables
- `FRAHOOSH_SCHOOL_ID`
- `FRAHOOSH_SCHOOL_NAME`
- `FRAHOOSH_SCHOOL_YEAR`

هرگز `service_role` key را در APK یا Repository قرار ندهید.

## تست قبل از Build
```bash
python -m compileall -q mobile
```

این دستور باید بدون خروجی خطا و با exit code صفر تمام شود.

## نکته مهم درباره پنل‌ها
این نسخه هسته Login، Loading، Session، Role routing و Navigation پنل‌ها را سالم می‌کند. عملیات CRUD هر زیرپنل باید دقیقاً بر اساس schema و RLS نسخه Web v16.12 به API متصل شود؛ در این نسخه هیچ جدول فرضی یا داده جعلی ساخته نشده است.
