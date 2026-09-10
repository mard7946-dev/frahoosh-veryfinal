from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import threading


class DashboardScreen(Screen):

    def __init__(self, app_state=None, **kwargs):

        super().__init__(**kwargs)

        self.app_state = app_state


    def on_enter(self):

        print(
            "DASHBOARD OPEN"
        )

        self.load_dashboard()



    def load_dashboard(self):

        try:

            self.ids.status.text = (
                "در حال دریافت اطلاعات..."
            )

        except:

            pass


        thread = threading.Thread(
            target=self._load_data
        )

        thread.start()



    def _load_data(self):

        try:

            user = None
            session = None


            if self.app_state:

                user = (
                    self.app_state.user
                )

                session = (
                    self.app_state.session
                )


            print(
                "CURRENT USER:",
                user
            )

            print(
                "SESSION:",
                session
            )


            if not session:

                Clock.schedule_once(
                    lambda dt:
                    self.set_status(
                        "نشست کاربر پیدا نشد"
                    )
                )

                return



            # اینجا اطلاعات پنل‌ها بعداً
            # از API خوانده می‌شود
            #
            # فعلاً هدف:
            # عبور صحیح از Login
            # و ساخت داشبورد است


            Clock.schedule_once(
                lambda dt:
                self.build_panels()
            )


        except Exception as exc:

            print(
                "DASHBOARD ERROR:",
                exc
            )

            Clock.schedule_once(
                lambda dt:
                self.set_status(
                    "خطا در ساخت داشبورد"
                )
            )



    def build_panels(
        self
    ):

        try:

            self.ids.status.text = (
                "داشبورد آماده شد"
            )


        except:

            pass


        print(
            "DASHBOARD READY"
        )



    def set_status(
        self,
        text
    ):

        try:

            self.ids.status.text = text

        except:

            pass
