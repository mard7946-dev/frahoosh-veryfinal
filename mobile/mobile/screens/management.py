from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

from mobile.config import (
    PRIMARY,
    SECONDARY,
    SUCCESS,
    WHITE,
)

from mobile.ui import (
    font_name,
    rtl_text,
)


class ManagementScreen(Screen):

    def __init__(
        self,
        app_state,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.app_state = app_state

        self.build_ui()



    def build_ui(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12)
        )


        title = Label(
            text=rtl_text(
                "پنل مدیریت مدرسه"
            ),
            font_name=font_name(),
            font_size="26sp",
            color=PRIMARY,
            size_hint_y=None,
            height=dp(55)
        )


        root.add_widget(title)



        info = Label(
            text=rtl_text(
                "سامانه هوشمند آموزشی یکپارچه فراهوش\n"
                "مدیریت کامل مدرسه"
            ),
            font_name=font_name(),
            font_size="15sp",
            color=SECONDARY,
            size_hint_y=None,
            height=dp(70)
        )


        root.add_widget(info)



        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None
        )


        grid.bind(
            minimum_height=grid.setter(
                "height"
            )
        )


        modules = [

            (
                "اطلاعات مدرسه",
                "school_info"
            ),

            (
                "کاربران و دسترسی‌ها",
                "users"
            ),

            (
                "مدیریت کارکنان",
                "staff"
            ),

            (
                "گزارش مدیریتی",
                "reports"
            ),

            (
                "تنظیمات سامانه",
                "settings"
            ),

            (
                "سال تحصیلی",
                "academic_year"
            ),

        ]



        for title, key in modules:


            btn = Button(
                text=rtl_text(title),
                font_name=font_name(),
                background_normal="",
                background_color=SUCCESS,
                color=WHITE,
                size_hint_y=None,
                height=dp(55)
            )


            btn.bind(
                on_release=lambda x,
                t=title,
                k=key:
                self.open_panel(
                    t,
                    k
                )
            )


            grid.add_widget(btn)



        root.add_widget(grid)



        back = Button(
            text=rtl_text(
                "بازگشت به داشبورد"
            ),
            font_name=font_name(),
            background_normal="",
            background_color=PRIMARY,
            color=WHITE,
            size_hint_y=None,
            height=dp(52)
        )


        back.bind(
            on_release=self.back
        )


        root.add_widget(back)


        self.add_widget(root)



    def open_panel(
        self,
        title,
        key
    ):

        if key == "settings":

            if not self.manager.has_screen(
                "settings"
            ):

                from mobile.screens.settings import (
                    SettingsScreen
                )

                self.manager.add_widget(
                    SettingsScreen(
                        self.app_state,
                        name="settings"
                    )
                )


            self.manager.current = (
                "settings"
            )

            return


        print(
            "MANAGEMENT PANEL:",
            key
        )



    def back(
        self,
        *_
    ):

        self.manager.current = (
            "dashboard"
        )
