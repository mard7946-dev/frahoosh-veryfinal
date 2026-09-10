import threading

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from mobile.services.api import APIService
from mobile.services.session import SessionManager


class LoginScreen(Screen):

    def __init__(self, app_state=None, **kwargs):

        super().__init__(**kwargs)

        self.app_state = app_state

        self.api = APIService()

        self.session = SessionManager()


    def login(self):

        national_code = self.ids.national_code.text.strip()
        password = self.ids.password.text.strip()


        if not national_code or not password:

            self.show_message(
                "کد ملی و رمز عبور را وارد کنید"
            )

            return


        self.show_message(
            "در حال اتصال..."
        )


        thread = threading.Thread(
            target=self._do_login,
            args=(
                national_code,
                password
            )
        )

        thread.start()



    def _do_login(
        self,
        national_code,
        password
    ):

        try:

            result = self.api.login(
                national_code,
                password
            )


            if not result:

                Clock.schedule_once(
                    lambda dt:
                    self.show_message(
                        "ورود ناموفق بود"
                    )
                )

                return



            access_token = result.get(
                "access_token"
            )

            refresh_token = result.get(
                "refresh_token"
            )


            if not access_token:

                Clock.schedule_once(
                    lambda dt:
                    self.show_message(
                        "توکن دریافت نشد"
                    )
                )

                return



            self.session.save_session(
                {
                    "access_token":
                        access_token,

                    "refresh_token":
                        refresh_token,

                    "user":
                        result.get(
                            "user"
                        )
                }
            )



            if self.app_state:

                self.app_state.session = result

                self.app_state.user = (
                    result.get(
                        "user"
                    )
                )



            Clock.schedule_once(
                self.open_dashboard
            )


        except Exception as exc:


            Clock.schedule_once(
                lambda dt:
                self.show_message(
                    "خطا در اتصال: "
                    + str(exc)
                )
            )



    def open_dashboard(
        self,
        dt
    ):

        if self.manager.has_screen(
            "dashboard"
        ):

            self.manager.current = (
                "dashboard"
            )

        else:

            self.show_message(
                "داشبورد موجود نیست"
            )



    def show_message(
        self,
        text
    ):

        print(
            text
        )

        try:

            self.ids.message.text = text

        except:

            pass
