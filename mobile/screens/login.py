import threading

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from mobile.config import APP_NAME, SYSTEM_TITLE, LOGO_PATH, PRIMARY, SECONDARY, SUCCESS, ERROR, WHITE
from mobile.services.api import APIService
from mobile.ui import font_name, rtl_text


class LoginScreen(Screen):
    """Programmatic login screen; no KV file or implicit ids required."""

    def __init__(self, app_state=None, **kwargs):
        super().__init__(**kwargs)
        self.app_state = app_state
        self.api = app_state.api if app_state and app_state.api else APIService()
        self._busy = False
        self.national_code = None
        self.password = None
        self.message = None
        self.login_button = None
        self._build()

    def _label(self, text, size="14sp", color=SECONDARY, height=dp(40), bold=False):
        label = Label(
            text=rtl_text(text), font_name=font_name(), font_size=size,
            color=color, bold=bold, halign="right", valign="middle",
            size_hint_y=None, height=height,
        )
        label.bind(size=lambda obj, value: setattr(obj, "text_size", value))
        return label

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(28), spacing=dp(12))
        root.add_widget(Label(size_hint_y=.18))
        root.add_widget(self._label(APP_NAME, "32sp", PRIMARY, dp(55), True))
        root.add_widget(self._label(SYSTEM_TITLE, "15sp", SECONDARY, dp(42)))

        form = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None, height=dp(205))
        form.add_widget(self._label("کد ملی / نام کاربری", "14sp", PRIMARY, dp(30), True))
        self.national_code = TextInput(
            multiline=False, font_name=font_name(), font_size="17sp", halign="right",
            size_hint_y=None, height=dp(50), padding=[dp(12), dp(12)],
        )
        form.add_widget(self.national_code)
        form.add_widget(self._label("رمز عبور", "14sp", PRIMARY, dp(30), True))
        self.password = TextInput(
            multiline=False, password=True, font_name=font_name(), font_size="17sp", halign="right",
            size_hint_y=None, height=dp(50), padding=[dp(12), dp(12)],
        )
        form.add_widget(self.password)
        root.add_widget(form)

        self.login_button = Button(
            text=rtl_text("ورود به فراهوش"), font_name=font_name(), font_size="16sp",
            background_normal="", background_color=SUCCESS, color=WHITE,
            size_hint_y=None, height=dp(55),
        )
        self.login_button.bind(on_release=lambda *_: self.login())
        root.add_widget(self.login_button)

        self.message = self._label("", "12sp", ERROR, dp(60))
        root.add_widget(self.message)
        root.add_widget(Label(size_hint_y=.35))
        self.add_widget(root)

    def on_pre_enter(self, *args):
        if self.app_state and self.app_state.logged_in and self.manager and self.manager.has_screen("dashboard"):
            self.manager.current = "dashboard"
        return super().on_pre_enter(*args)

    def login(self):
        if self._busy:
            return
        national_code = self.national_code.text.strip()
        password = self.password.text
        if not national_code or not password:
            self.show_message("کد ملی و رمز عبور را وارد کنید.", ERROR)
            return
        if not self.api.configured:
            self.show_message("اتصال سرور در این نسخه تنظیم نشده است.", ERROR)
            return

        self._busy = True
        self.login_button.disabled = True
        self.show_message("در حال اتصال و احراز هویت...", SECONDARY)
        threading.Thread(target=self._do_login, args=(national_code, password), daemon=True).start()

    def _do_login(self, national_code, password):
        try:
            result = self.api.login(national_code, password)
            if not result or not result.get("access_token"):
                Clock.schedule_once(lambda dt: self._finish("ورود ناموفق بود؛ اطلاعات ورود را بررسی کنید.", ERROR))
                return
            if self.app_state is None or not self.app_state.set_session(result):
                Clock.schedule_once(lambda dt: self._finish("ذخیره نشست کاربر ناموفق بود.", ERROR))
                return
            Clock.schedule_once(lambda dt: self._open_dashboard())
        except Exception as exc:
            message = str(exc) or "خطای ناشناخته"
            Clock.schedule_once(lambda dt, msg=message: self._finish(f"خطا در اتصال به سرور: {msg}", ERROR))

    def _finish(self, message, color):
        self._busy = False
        self.login_button.disabled = False
        self.show_message(message, color)

    def _open_dashboard(self):
        self._busy = False
        self.login_button.disabled = False
        if self.manager and self.manager.has_screen("dashboard"):
            self.manager.current = "dashboard"
        else:
            self.show_message("داشبورد موجود نیست.", ERROR)

    def show_message(self, text, color=ERROR):
        print(text)
        if self.message:
            self.message.text = rtl_text(text)
            self.message.color = color
