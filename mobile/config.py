import json
import os
from pathlib import Path


# ============================================================
# Frahoosh Mobile - Configuration
# ============================================================

APP_NAME = "فراهوش"
SYSTEM_TITLE = "سامانه هوشمند آموزشی یکپارچه"

APP_VERSION = "1.1.1"

PACKAGE_NAME = "ir.frahoosh"
DEVELOPER_NAME = "تیم توسعه فراهوش"


# ============================================================
# Base Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"

RUNTIME_CONFIG_FILE = BASE_DIR / "runtime_config.json"


# ============================================================
# Runtime Configuration
# ============================================================

def _read_runtime_config():
    """
    خواندن تنظیمات قابل تغییر بدون ایجاد خطا.
    """

    try:
        if not RUNTIME_CONFIG_FILE.exists():
            return {}

        text = RUNTIME_CONFIG_FILE.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            return {}

        data = json.loads(text)

        if isinstance(data, dict):
            return data

    except Exception as exc:
        print(
            "Runtime config read error:",
            repr(exc)
        )

    return {}


_RUNTIME = _read_runtime_config()


def _setting(name, default=""):
    """
    دریافت تنظیمات به ترتیب اولویت:

    1. Environment
    2. runtime_config.json
    3. مقدار پیش‌فرض
    """

    try:
        value = os.getenv(name)

        if value is not None:
            value = str(value).strip()

            if value:
                return value

    except Exception:
        pass

    try:
        value = _RUNTIME.get(
            name,
            default
        )

        if value is None:
            return default

        value = str(value).strip()

        if value:
            return value

    except Exception:
        pass

    return default


# ============================================================
# Backend / Supabase
# ============================================================

SUPABASE_URL = _setting(
    "FRAHOOSH_SUPABASE_URL",
    ""
).rstrip("/")


SUPABASE_ANON_KEY = _setting(
    "FRAHOOSH_SUPABASE_ANON_KEY",
    "")


# ============================================================
# School Configuration
# ============================================================

SCHOOL_ID = _setting(
    "FRAHOOSH_SCHOOL_ID",
    "frahoosh-school"
)


SCHOOL_NAME = _setting(
    "FRAHOOSH_SCHOOL_NAME",
    "دبیرستان سردار شهید حاجی‌زاده ۲"
)


SCHOOL_YEAR = _setting(
    "FRAHOOSH_SCHOOL_YEAR",
    "۱۴۰۵ - ۱۴۰۶"
)


# ============================================================
# API Configuration
# ============================================================

def _get_timeout():
    try:
        value = float(
            _setting(
                "FRAHOOSH_API_TIMEOUT",
                "15"
            )
        )

        if value <= 0:
            return 15

        return value

    except Exception:
        return 15


API_TIMEOUT = _get_timeout()


# ============================================================
# Assets
# ============================================================

FONT_REGULAR = str(
    ASSETS_DIR /
    "NotoSansArabic-Regular.ttf"
)


FONT_BOLD = str(
    ASSETS_DIR /
    "NotoSansArabic-Bold.ttf"
)


LOGO_PATH = str(
    ASSETS_DIR /
    "frahoosh_logo.png"
)


# ============================================================
# Asset Validation
# ============================================================

FONT_REGULAR_EXISTS = Path(
    FONT_REGULAR
).exists()


FONT_BOLD_EXISTS = Path(
    FONT_BOLD
).exists()


LOGO_EXISTS = Path(
    LOGO_PATH
).exists()


# ============================================================
# UI Colors
# ============================================================

PRIMARY = (
    0.059,
    0.090,
    0.165,
    1
)


SECONDARY = (
    0.118,
    0.227,
    0.545,
    1
)


SUCCESS = (
    0.086,
    0.639,
    0.325,
    1
)


BACKGROUND = (
    0.965,
    0.975,
    0.985,
    1
)


WHITE = (
    1,
    1,
    1,
    1
)


TEXT = (
    0.08,
    0.10,
    0.14,
    1
)


MUTED = (
    0.38,
    0.42,
    0.48,
    1
)


ERROR = (
    0.75,
    0.12,
    0.12,
    1
)


CARD = (
    1,
    1,
    1,
    1
)


BORDER = (
    0.86,
    0.89,
    0.93,
    1
)


# ============================================================
# Compatibility Aliases
# ============================================================

# برای جلوگیری از خطا در فایل‌های قدیمی پروژه

BACKGROUND_COLOR = BACKGROUND

TEXT_COLOR = TEXT

MUTED_COLOR = MUTED

CARD_COLOR = CARD

BORDER_COLOR = BORDER

PRIMARY_COLOR = PRIMARY

SECONDARY_COLOR = SECONDARY

SUCCESS_COLOR = SUCCESS

ERROR_COLOR = ERROR

WHITE_COLOR = WHITE


# ============================================================
# Debug Information
# ============================================================

def print_config_status():
    """
    نمایش وضعیت تنظیمات فقط برای محیط توسعه.
    """

    print(
        "========================================"
    )

    print(
        "Frahoosh Mobile Configuration"
    )

    print(
        "APP:",
        APP_NAME
    )

    print(
        "VERSION:",
        APP_VERSION
    )

    print(
        "SCHOOL:",
        SCHOOL_NAME
    )

    print(
        "SCHOOL YEAR:",
        SCHOOL_YEAR
    )

    print(
        "SUPABASE:",
        "CONFIGURED"
        if SUPABASE_URL and SUPABASE_ANON_KEY
        else "NOT CONFIGURED"
    )

    print(
        "FONT REGULAR:",
        "OK"
        if FONT_REGULAR_EXISTS
        else "MISSING"
    )

    print(
        "FONT BOLD:",
        "OK"
        if FONT_BOLD_EXISTS
        else "MISSING"
    )

    print(
        "LOGO:",
        "OK"
        if LOGO_EXISTS
        else "MISSING"
    )

    print(
        "========================================"
    )


# ============================================================
# Safe Startup Check
# ============================================================

try:
    print_config_status()
except Exception as exc:
    print(
        "Configuration status error:",
        repr(exc)
    )
