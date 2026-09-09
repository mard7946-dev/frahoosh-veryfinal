from threading import Thread

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from mobile.config import (
    APP_NAME,
    SYSTEM_TITLE,
    SCHOOL_NAME,
    PRIMARY,
    SECONDARY,
    SUCCESS,
    WHITE,
    ERROR,
)

from mobile.ui import (
    font_name,
    rtl_text,
    PersianTextInput,
)


class LoginScreen(Screen):

    def __init__(
        self,
        app_state,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.app_state = app_state
        self._busy = False
        self._login_generation = 0

        self._build()

    # ========================================================
    # BUILD UI
    # ========================================================

    def _build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(12),
        )

        # ----------------------------------------------------
        # App name
        # ----------------------------------------------------

        title = Label(
            text=rtl_text(APP_NAME),
            font_name=font_name(),
            font_size="36sp",
            bold=True,
            color=PRIMARY,
            size_hint_y=None,
            height=dp(60),
            halign="center",
            valign="middle",
        )

        title.bind(
            size=self._sync_text
        )

        root.add_widget(title)

        # ----------------------------------------------------
        # System title
        # ----------------------------------------------------

        subtitle = Label(
            text=rtl_text(SYSTEM_TITLE),
            font_name=font_name(),
            font_size="17sp",
            color=SECONDARY,
            size_hint_y=None,
            height=dp(42),
            halign="center",
            valign="middle",
        )

        subtitle.bind(
            size=self._sync_text
        )

        root.add_widget(subtitle)

        # ----------------------------------------------------
        # School name
        # ----------------------------------------------------

        school = Label(
            text=rtl_text(SCHOOL_NAME),
            font_name=font_name(),
            font_size="13sp",
            color=PRIMARY,
            size_hint_y=None,
            height=dp(38),
            halign="center",
            valign="middle",
        )

        school.bind(
            size=self._sync_text
        )

        root.add_widget(school)

        # ----------------------------------------------------
        # National code
        # ----------------------------------------------------

        self.identifier = PersianTextInput(
            hint_text=rtl_text(
                "کد ملی"
            ),
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(54),
            halign="right",
            padding=[
                dp(12),
                dp(10),
                dp(12),
                dp(10),
            ],
        )

        root.add_widget(
            self.identifier
        )

        # ----------------------------------------------------
        # Password
        # ----------------------------------------------------

        self.password = PersianTextInput(
            hint_text=rtl_text(
                "رمز عبور"
            ),
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(54),
            halign="right",
            padding=[
                dp(12),
                dp(10),
                dp(12),
                dp(10),
            ],
        )

        root.add_widget(
            self.password
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        self.status = Label(
            text="",
            font_name=font_name(),
            font_size="13sp",
            color=SECONDARY,
            size_hint_y=None,
            height=dp(55),
            halign="center",
            valign="middle",
        )

        self.status.bind(
            size=self._sync_text
        )

        root.add_widget(
            self.status
        )

        # ----------------------------------------------------
        # Login button
        # ----------------------------------------------------

        self.login_button = Button(
            text=rtl_text(
                "ورود به فراهوش"
            ),
            font_name=font_name(),
            font_size="17sp",
            background_normal="",
            background_color=SUCCESS,
            color=WHITE,
            size_hint_y=None,
            height=dp(56),
        )

        self.login_button.bind(
            on_release=self.login
        )

        root.add_widget(
            self.login_button
        )

        self.add_widget(
            root
        )

    # ========================================================
    # TEXT
    # ========================================================

    def _sync_text(
        self,
        obj,
        value
    ):
        obj.text_size = value

    # ========================================================
    # STATUS
    # ========================================================

    def _set_status(
        self,
        text,
        color=SECONDARY
    ):
        try:
            self.status.text = rtl_text(
                text
            )

            self.status.color = color

        except Exception as exc:
            print(
                "LOGIN STATUS ERROR:",
                repr(exc)
            )

    # ========================================================
    # INPUT NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize_digits(value):

        text = str(
            value or ""
        )

        replacements = {
            "۰": "0",
            "۱": "1",
            "۲": "2",
            "۳": "3",
            "۴": "4",
            "۵": "5",
            "۶": "6",
            "۷": "7",
            "۸": "8",
            "۹": "9",
            "٠": "0",
            "١": "1",
            "٢": "2",
            "٣": "3",
            "٤": "4",
            "٥": "5",
            "٦": "6",
            "٧": "7",
            "٨": "8",
            "٩": "9",
        }

        for old, new in replacements.items():
            text = text.replace(
                old,
                new
            )

        return text

    # ========================================================
    # LOGIN
    # ========================================================

    def login(
        self,
        *_ 
    ):

        if self._busy:
            return

        if self.app_state is None:

            self._set_status(
                "وضعیت برنامه آماده نیست.",
                ERROR
            )

            return

        code = self._normalize_digits(
            self.identifier.text
        ).strip()

        password = str(
            self.password.text or ""
        )

        # ----------------------------------------------------
        # Validate national code
        # ----------------------------------------------------

        if not code:

            self._set_status(
                "کد ملی را وارد کنید.",
                ERROR
            )

            return

        if len(code) != 10:

            self._set_status(
                "کد ملی باید ۱۰ رقم باشد.",
                ERROR
            )

            return

        if not code.isdigit():

            self._set_status(
                "کد ملی فقط باید شامل عدد باشد.",
                ERROR
            )

            return

        # ----------------------------------------------------
        # Validate password
        # ----------------------------------------------------

        if not password:

            self._set_status(
                "رمز عبور را وارد کنید.",
                ERROR
            )

            return

        # ----------------------------------------------------
        # API check
        # ----------------------------------------------------

        try:
            api = self.app_state.api

        except Exception as exc:

            print(
                "API ACCESS ERROR:",
                repr(exc)
            )

            api = None

        if api is None:

            self._set_status(
                "اتصال سرور آماده نیست.",
                ERROR
            )

            return

        # ----------------------------------------------------
        # Start authentication
        # ----------------------------------------------------

        self._busy = True

        self._login_generation += 1

        generation = (
            self._login_generation
        )

        self.login_button.disabled = True

        self._set_status(
            "در حال بررسی اطلاعات..."
        )

        Thread(
            target=self._authenticate,
            args=(
                code,
                password,
                generation,
            ),
            daemon=True,
        ).start()

    # ========================================================
    # AUTHENTICATION THREAD
    # ========================================================

    def _authenticate(
        self,
        code,
        password,
        generation,
    ):

        try:

            session = self.app_state.api.sign_in(
                code,
                password
            )

            if not session:
                raise Exception(
                    "نشست کاربر دریافت نشد."
                )

            # ------------------------------------------------
            # Validate returned session
            # ------------------------------------------------

            if not isinstance(
                session,
                dict
            ):
                raise Exception(
                    "پاسخ احراز هویت نامعتبر است."
                )

            # ------------------------------------------------
            # Save session
            # ------------------------------------------------

            saved = self.app_state.set_session(
                session
            )

            if not saved:
                raise Exception(
                    "ذخیره نشست انجام نشد."
                )

            # ------------------------------------------------
            # Return to Kivy main thread
            # ------------------------------------------------

            Clock.schedule_once(
                lambda dt: self._login_success(
                    generation
                ),
                0
            )

        except Exception as exc:

            print(
                "AUTH ERROR:",
                repr(exc)
            )

            message = str(
                exc
            ).strip()

            if not message:
                message = (
                    "ورود به سامانه انجام نشد."
                )

            Clock.schedule_once(
                lambda dt: self._login_failed(
                    message,
                    generation,
                ),
                0
            )

    # ========================================================
    # LOGIN SUCCESS
    # ========================================================

    def _login_success(
        self,
        generation,
    ):

        if generation != self._login_generation:
            return

        self._busy = False

        try:
            self.login_button.disabled = False
        except Exception:
            pass

        self._set_status(
            "ورود موفق بود.",
            SUCCESS
        )

        # ----------------------------------------------------
        # ScreenManager
        # ----------------------------------------------------

        manager = self.manager

        if manager is None:

            print(
                "DASHBOARD OPEN ERROR: "
                "ScreenManager موجود نیست."
            )

            self._set_status(
                "ورود موفق شد اما برنامه آماده نمایش داشبورد نیست.",
                ERROR
            )

            return

        # ----------------------------------------------------
        # Dashboard existence
        # ----------------------------------------------------

        try:
            exists = manager.has_screen(
                "dashboard"
            )

        except Exception as exc:

            print(
                "SCREEN CHECK ERROR:",
                repr(exc)
            )

            exists = False

        if not exists:

            print(
                "DASHBOARD OPEN ERROR: "
                "Dashboard ساخته نشده است."
            )

            self._set_status(
                "ورود موفق شد اما داشبورد ساخته نشده است.",
                ERROR
            )

            return

        # ----------------------------------------------------
        # Get dashboard
        # ----------------------------------------------------

        try:

            dashboard = manager.get_screen(
                "dashboard"
            )

        except Exception as exc:

            print(
                "DASHBOARD GET ERROR:",
                repr(exc)
            )

            self._set_status(
                "ورود موفق شد اما داشبورد قابل دریافت نیست.",
                ERROR
            )

            return

        # ----------------------------------------------------
        # Refresh dashboard safely
        # ----------------------------------------------------

        try:

            refresh = getattr(
                dashboard,
                "refresh",
                None
            )

            if callable(refresh):

                refresh()

        except Exception as exc:

            # Dashboard refresh must never prevent
            # navigation after successful login.
            print(
                "DASHBOARD REFRESH ERROR:",
                repr(exc)
            )

        # ----------------------------------------------------
        # Open dashboard
        # ----------------------------------------------------

        try:

            manager.current = (
                "dashboard"
            )

            print(
                "LOGIN SUCCESS -> DASHBOARD"
            )

        except Exception as exc:

            print(
                "DASHBOARD NAVIGATION ERROR:",
                repr(exc)
            )

            self._set_status(
                "ورود موفق شد اما انتقال به داشبورد انجام نشد.",
                ERROR
            )

    # ========================================================
    # LOGIN FAILED
    # ========================================================

    def _login_failed(
        self,
        message,
        generation,
    ):

        if generation != self._login_generation:
            return

        self._busy = False

        try:
            self.login_button.disabled = False
        except Exception:
            pass

        self._set_status(
            message,
            ERROR
        )

    # ========================================================
    # SCREEN ENTER
    # ========================================================

    def on_pre_enter(
        self,
        *args
    ):

        self._busy = False

        self._login_generation += 1

        try:
            self.login_button.disabled = False
        except Exception:
            pass

        return super().on_pre_enter(
            *args
        )

    # ========================================================
    # SCREEN LEAVE
    # ========================================================

    def on_leave(
        self,
        *args
    ):

        # Do not cancel an active successful authentication
        # merely because Kivy is transitioning screens.
        try:
            self.login_button.disabled = False
        except Exception:
            pass

        return super().on_leave(
            *args
        )
