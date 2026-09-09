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


class SchoolScreen(Screen):

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
            padding=dp(20),
            spacing=dp(15),
        )


        title = Label(
            text=rtl_text(
                "مدیریت مدرسه"
            ),
            font_name=font_name(),
            font_size="28sp",
            color=PRIMARY,
            size_hint_y=None,
            height=dp(50),
        )

        root.add_widget(title)


        info = Label(
            text=rtl_text(
                "دبیرستان سردار شهید حاجی زاده ۲\n"
                "سامانه هوشمند آموزشی یکپارچه فراهوش"
            ),
            font_name=font_name(),
            font_size="16sp",
            color=SECONDARY,
            size_hint_y=None,
            height=dp(80),
        )

        root.add_widget(info)


        menu = GridLayout(
            cols=2,
            spacing=dp(12),
            size_hint_y=None,
        )

        menu.bind(
            minimum_height=menu.setter(
                "height"
            )
        )


        buttons = [

            "اطلاعات مدرسه",

            "کاربران و دسترسی‌ها",

            "مدیریت کارکنان",

            "تنظیمات سامانه",

            "گزارش مدیریتی",

            "سال تحصیلی",

        ]


        for item in buttons:

            btn = Button(
                text=rtl_text(item),
                font_name=font_name(),
                background_normal="",
                background_color=SUCCESS,
                color=WHITE,
                size_hint_y=None,
                height=dp(55),
            )

            btn.bind(
                on_release=lambda x, name=item:
                self.open_module(name)
            )


            menu.add_widget(btn)


        root.add_widget(menu)


        back = Button(
            text=rtl_text(
                "بازگشت"
            ),
            font_name=font_name(),
            background_normal="",
            background_color=PRIMARY,
            color=WHITE,
            size_hint_y=None,
            height=dp(50),
        )


        back.bind(
            on_release=self.go_back
        )


        root.add_widget(back)


        self.add_widget(root)



    def open_module(
        self,
        name
    ):

        print(
            "SCHOOL MODULE:",
            name
        )



    def go_back(
        self,
        *_ 
    ):

        self.manager.current = (
            "dashboard"
        )
