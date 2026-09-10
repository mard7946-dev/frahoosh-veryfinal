from kivy.animation import Animation
from kivy.graphics import (
    Color,
    RoundedRectangle,
    Rectangle,
    Line,
)
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView

from mobile.config import (
    APP_NAME,
    SCHOOL_NAME,
    BACKGROUND_PATH,
    PRIMARY,
)

from mobile.ui import (
    font_name,
    rtl_text,
)


ROLE_ALIASES = {

    "admin": "manager",
    "administrator": "manager",
    "manager": "manager",
    "مدیر": "manager",
    "مدیریت": "manager",

    "executive": "executive",
    "معاون اجرایی": "executive",

    "educational": "educational",
    "training": "educational",
    "معاون آموزشی": "educational",

    "cultural": "cultural",
    "پرورشی": "cultural",
    "معاون پرورشی": "cultural",

    "advisor": "advisor",
    "counselor": "advisor",
    "مشاور": "advisor",
    "مشاوره": "advisor",

    "teacher": "teacher",
    "teacher_staff": "teacher",
    "دبیر": "teacher",
    "معلم": "teacher",

    "student": "student",
    "دانش‌آموز": "student",
    "دانش آموز": "student",

    "parent": "parent",
    "parent_guardian": "parent",
    "guardian": "parent",
    "ولی": "parent",
    "اولیا": "parent",
}


ROLE_TITLES = {

    "manager": "مدیریت",
    "executive": "معاون اجرایی",
    "educational": "معاون آموزشی",
    "cultural": "معاون پرورشی",
    "advisor": "مشاوره",
    "teacher": "دبیر",
    "student": "دانش‌آموز",
    "parent": "ولی",
}


MANAGER_MENU = [

    ("مدیریت", "management"),
    ("معاون آموزشی", "educational"),
    ("معاون اجرایی", "executive"),
    ("معاون پرورشی", "cultural"),
    ("مشاوره", "advisor"),
    ("دبیران", "teachers"),
    ("اولیا", "parents"),
    ("دانش‌آموزان", "students"),
    ("مالی", "finance"),
    ("پرداخت آنلاین", "payment"),
    ("کلاس‌های آنلاین", "online"),
    ("تابلو هوشمند", "smart_board"),
    ("دستیار هوش مصنوعی", "ai"),
    ("گزارش‌ها", "reports"),
    ("صندوق پیام‌ها", "messages"),
    ("تنظیمات", "settings"),
    ("درباره برنامه", "about"),
]


ROLE_MENU = {

    "executive": [
        ("معاون اجرایی", "executive"),
        ("دانش‌آموزان", "students"),
        ("اولیا", "parents"),
        ("صندوق پیام‌ها", "messages"),
        ("تنظیمات", "settings"),
        ("درباره برنامه", "about"),
    ],

    "educational": [
        ("معاون آموزشی", "educational"),
        ("دانش‌آموزان", "students"),
        ("دبیران", "teachers"),
        ("کلاس‌های آنلاین", "online"),
        ("تابلو هوشمند", "smart_board"),
        ("گزارش‌ها", "reports"),
        ("صندوق پیام‌ها", "messages"),
        ("درباره برنامه", "about"),
    ],

    id="r2s9kq"
    "cultural": [
        ("معاون پرورشی", "cultural"),
        ("فعالیت‌های فرهنگی", "cultural_activity"),
        ("دانش‌آموزان", "students"),
        ("اولیا", "parents"),
        ("گزارش‌ها", "reports"),
        ("پیام‌ها", "messages"),
        ("درباره برنامه", "about"),
    ],

    "advisor": [
        ("مشاوره", "advisor"),
        ("پرونده دانش‌آموزان", "students"),
        ("گزارش مشاوره", "reports"),
        ("پیام‌ها", "messages"),
        ("درباره برنامه", "about"),
    ],

    "teacher": [
        ("کلاس‌های من", "my_classes"),
        ("دانش‌آموزان", "students"),
        ("حضور و غیاب", "attendance"),
        ("نمرات", "grades"),
        ("تکالیف", "homework"),
        ("کلاس آنلاین", "online"),
        ("پیام‌ها", "messages"),
        ("درباره برنامه", "about"),
    ],

    "student": [
        ("کلاس‌های من", "my_classes"),
        ("برنامه هفتگی", "schedule"),
        ("نمرات", "grades"),
        ("تکالیف", "homework"),
        ("کلاس آنلاین", "online"),
        ("پیام‌ها", "messages"),
        ("درباره برنامه", "about"),
    ],

    "parent": [
        ("فرزند من", "children"),
        ("حضور و غیاب", "attendance"),
        ("نمرات", "grades"),
        ("پرداخت‌ها", "payment"),
        ("پیام‌ها", "messages"),
        ("درباره برنامه", "about"),
    ],

}


class DashboardBackground(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        with self.canvas.before:

            Color(
                0.96,
                0.97,
                0.99,
                1
            )

            self.rect = RoundedRectangle(
                radius=[
                    (20, 20),
                    (20, 20),
                    (20, 20),
                    (20, 20),
                ]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )


    def update_rect(
        self,
        *args
    ):

        self.rect.pos = self.pos
        self.rect.size = self.size



class MenuButton(Button):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.font_name = font_name

        self.font_size = dp(15)

        self.background_normal = ""

        self.background_color = (
            0,
            0,
            0,
            0
        )

        with self.canvas.before:

            self.bg_color = Color(
                0.12,
                0.45,
                0.85,
                0.15
            )

            self.bg = RoundedRectangle(
                radius=[
                    (12,12),
                    (12,12),
                    (12,12),
                    (12,12)
                ]
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )


    def update_bg(
        self,
        *args
    ):

        self.bg.pos = self.pos

        self.bg.size = self.size

class DashboardScreen(Screen):

    def __init__(
        self,
        app_state=None,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.app_state = app_state

        self.user = None

        self.role = None

        self.menu_items = []


    def on_enter(self):

        print(
            "ENTER DASHBOARD"
        )

        self.load_user()



    def load_user(self):

        try:

            if self.app_state:

                self.user = (
                    self.app_state.user
                )


            if not self.user:

                print(
                    "USER NOT FOUND"
                )

                return


            role = (
                self.user.get(
                    "role"
                )
                or
                self.user.get(
                    "user_role"
                )
                or
                self.user.get(
                    "type"
                )
            )


            self.role = self.normalize_role(
                role
            )


            self.create_dashboard()



        except Exception as exc:

            print(
                "LOAD USER ERROR:",
                exc
            )



    def normalize_role(
        self,
        role
    ):

        if not role:

            return "student"


        role = str(
            role
        ).lower().strip()


        return ROLE_ALIASES.get(
            role,
            role
        )



    def create_dashboard(
        self
    ):

        try:

            title = ROLE_TITLES.get(
                self.role,
                "کاربر"
            )


            print(
                "ROLE:",
                self.role
            )


            if self.role == "manager":

                self.menu_items = (
                    MANAGER_MENU
                )

            else:

                self.menu_items = (
                    ROLE_MENU.get(
                        self.role,
                        []
                    )
                )


            self.build_ui(
                title
            )


        except Exception as exc:

            print(
                "CREATE DASHBOARD ERROR:",
                exc
            )



    def build_ui(
        self,
        title
    ):

        self.clear_widgets()


        root = FloatLayout()


        background = DashboardBackground()

        root.add_widget(
            background
        )


        header = Label(

            text=rtl_text(
                title
            ),

            font_name=font_name,

            font_size=dp(22),

            size_hint=(
                1,
                None
            ),

            height=dp(70),

            pos_hint={
                "top": 1
            }

        )


        root.add_widget(
            header
        )


        scroll = ScrollView(

            size_hint=(
                .9,
                .75
            ),

            pos_hint={
                "center_x": .5,
                "center_y": .45
            }

        )


        container = FloatLayout(
            size_hint_y=None
        )


        container.height = (
            len(self.menu_items)
            *
            dp(65)
        )


        y = container.height - dp(65)


        for title, module in self.menu_items:


            button = MenuButton(

                text=rtl_text(
                    title
                ),

                size_hint=(
                    .9,
                    None
                ),

                height=dp(55),

                pos=(
                    dp(20),
                    y
                )

            )


            button.bind(
                on_release=lambda btn,
                m=module:
                self.open_module(m)
            )


            container.add_widget(
                button
            )


            y -= dp(65)


        scroll.add_widget(
            container
        )


        root.add_widget(
            scroll
        )


        self.add_widget(
            root
        )

    def open_module(
        self,
        module
    ):

        print(
            "OPEN MODULE:",
            module
        )


        if not self.manager:

            return


        if self.manager.has_screen(
            "module"
        ):

            module_screen = (
                self.manager.get_screen(
                    "module"
                )
            )


            try:

                module_screen.load_module(
                    module,
                    self.user
                )

            except Exception as exc:

                print(
                    "MODULE LOAD ERROR:",
                    exc
                )


            self.manager.current = (
                "module"
            )


        else:

            print(
                "MODULE SCREEN NOT FOUND"
            )



    def refresh(
        self
    ):

        print(
            "REFRESH DASHBOARD"
        )

        self.load_user()



    def logout(
        self
    ):

        print(
            "LOGOUT"
        )


        try:

            if self.app_state:

                self.app_state.user = None

                self.app_state.session = None


        except Exception as exc:

            print(
                "LOGOUT ERROR:",
                exc
            )


        if self.manager:

            if self.manager.has_screen(
                "login"
            ):

                self.manager.current = (
                    "login"
                )

    def update_user(
        self,
        user
    ):

        """
        بروزرسانی کاربر فعلی
        """

        self.user = user

        self.create_dashboard()



    def show_error(
        self,
        message
    ):

        print(
            "DASHBOARD ERROR:",
            message
        )



    def get_user_name(
        self
    ):

        if not self.user:

            return "کاربر"


        return (

            self.user.get(
                "full_name"
            )

            or

            self.user.get(
                "name"
            )

            or

            self.user.get(
                "email"
            )

            or

            "کاربر"

        )



    def get_role_title(
        self
    ):

        return ROLE_TITLES.get(
            self.role,
            "کاربر"
        )
