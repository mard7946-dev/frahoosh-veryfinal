import threading

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from mobile.services.api import APIService


class LoginScreen(Screen):
    def __init__(self, app_state=None, **kwargs):
        super().__init__(**kwargs)
        self.app_state = app_state
        self.api = app_state.api if app_state and app_state.api else APIService()
        self._busy = False

    def login(self):
        if self._busy:
            return

        national_code = self.ids.national_code.text.strip()
        password = self.ids.password.text

        if not national_code or not password:
            self.show_message("کد ملی و رمز عبور را وارد کنید")
            return

        self._busy = True
        self.show_message("در حال اتصال به سرور و ورود...")
        threading.Thread(
            target=self._do_login,
            args=(national_code, password),
            daemon=True,
        ).start()

    def _do_login(self, national_code, password):
        try:
            result = self.api.login(national_code, password)
            if not result or not result.get("access_token"):
                Clock.schedule_once(
                    lambda dt: self.show_message(
                        "ورود ناموفق است؛ کد ملی یا رمز عبور را بررسی کنید."
                    )
                )
                return

            if self.app_state is None:
                Clock.schedule_once(
                    lambda dt: self.show_message("وضعیت برنامه آماده نیست")
                )
                return

            if not self.app_state.set_session(result):
                Clock.schedule_once(
                    lambda dt: self.show_message("ذخیره نشست کاربر ناموفق بود")
                )
                return

            Clock.schedule_once(self.open_dashboard)
        except Exception as exc:
            message = str(exc) or "خطای ناشناخته"
            Clock.schedule_once(
                lambda dt, msg=message: self.show_message(
                    f"خطا در اتصال به سرور: {msg}"
                )
            )
        finally:
            self._busy = False

    def open_dashboard(self, dt=0):
        if self.manager and self.manager.has_screen("dashboard"):
            self.manager.current = "dashboard"
        else:
            self.show_message("داشبورد موجود نیست")

    def show_message(self, text):
        print(text)
        try:
            self.ids.message.text = text
        except Exception:
            pass
