from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

from mobile.config import (
    APP_NAME,
    SCHOOL_NAME,
    APP_VERSION,
    PRIMARY,
    SECONDARY,
    WHITE,
)

from mobile.ui import font_name, rtl_text


# =========================================================
# ROLE TITLES
# =========================================================

ROLE_TITLES = {
    "manager": "مدیریت مدرسه",
    "admin": "مدیریت مدرسه",
    "principal": "مدیریت مدرسه",

    "educational": "معاون آموزشی",
    "education": "معاون آموزشی",
    "assistant_education": "معاون آموزشی",

    "executive": "معاون اجرایی",
    "assistant_executive": "معاون اجرایی",

    "cultural": "معاون پرورشی",
    "assistant_cultural": "معاون پرورشی",
    "training": "معاون پرورشی",

    "advisor": "مشاوره",
    "counselor": "مشاوره",

    "teacher": "دبیر",
    "teachers": "دبیران",

    "student": "دانش‌آموز",
    "students": "دانش‌آموزان",

    "parent": "ولی دانش‌آموز",
    "parents": "اولیا",
}


# =========================================================
# ROLE MENUS
# =========================================================

ROLE_MENUS = {

    "manager": [
        ("🏫 مدیریت مدرسه", "management"),
        ("📚 معاون آموزشی", "educational"),
        ("🗂 معاون اجرایی", "executive"),
        ("🎯 معاون پرورشی", "cultural"),
        ("👥 دبیران", "teachers"),
        ("👨‍🎓 دانش‌آموزان", "students"),
        ("👨‍👩‍👦 اولیا", "parents"),
        ("💰 امور مالی", "finance"),
        ("💻 کلاس‌های آنلاین", "online"),
        ("🖥 تابلو هوشمند", "smart_board"),
        ("🤖 هوش مصنوعی", "ai"),
        ("📊 گزارش‌ها", "reports"),
        ("💬 پیام‌ها", "messages"),
        ("⚙️ تنظیمات", "settings"),
        ("📅 برنامه هفتگی", "schedule"),
        ("ℹ️ درباره فراهوش", "about"),
    ],


    "admin": [
        ("🏫 مدیریت مدرسه", "management"),
        ("👥 دبیران", "teachers"),
        ("👨‍🎓 دانش‌آموزان", "students"),
        ("👨‍👩‍👦 اولیا", "parents"),
        ("💰 امور مالی", "finance"),
        ("💻 کلاس‌های آنلاین", "online"),
        ("🖥 تابلو هوشمند", "smart_board"),
        ("🤖 هوش مصنوعی", "ai"),
        ("📊 گزارش‌ها", "reports"),
        ("⚙️ تنظیمات", "settings"),
    ],


    "educational": [
        ("📚 معاون آموزشی", "educational"),
        ("👨‍🎓 دانش‌آموزان", "students"),
        ("👥 دبیران", "teachers"),
        ("📅 برنامه هفتگی", "schedule"),
        ("📊 وضعیت تحصیلی", "student_info"),
        ("📈 گزارش‌ها", "reports"),
        ("💻 کلاس‌های آنلاین", "online"),
    ],


    "executive": [
        ("🗂 معاون اجرایی", "executive"),
        ("👨‍🎓 دانش‌آموزان", "students"),
        ("👨‍👩‍👦 اولیا", "parents"),
        ("💰 امور مالی", "finance"),
        ("📊 گزارش‌ها", "reports"),
        ("⚙️ تنظیمات", "settings"),
    ],


    "cultural": [
        ("🎯 معاون پرورشی", "cultural"),
        ("👨‍🎓 دانش‌آموزان", "students"),
        ("🖥 تابلو هوشمند", "smart_board"),
        ("💬 پیام‌ها", "messages"),
        ("📊 گزارش‌ها", "reports"),
    ],


    "teacher": [
        ("👨‍🏫 پنل دبیر", "teacher"),
        ("📅 برنامه هفتگی", "schedule"),
        ("👨‍🎓 دانش‌آموزان", "students"),
        ("💻 کلاس‌های آنلاین", "online"),
        ("📊 گزارش‌ها", "reports"),
        ("💬 پیام‌ها", "messages"),
    ],


    "student": [
        ("👨‍🎓 پنل دانش‌آموز", "student"),
        ("📅 برنامه هفتگی", "schedule"),
        ("📊 وضعیت تحصیلی", "student_info"),
        ("💻 کلاس آنلاین", "online"),
        ("💬 پیام‌ها", "messages"),
    ],


    "parent": [
        ("👨‍👩‍👦 پنل اولیا", "parent"),
        ("📊 وضعیت تحصیلی", "student_info"),
        ("💳 پرداخت‌ها", "payment"),
        ("💻 کلاس آنلاین", "online"),
        ("💬 پیام‌ها", "messages"),
    ],
}


# =========================================================
# DASHBOARD SCREEN
# =========================================================

class DashboardScreen(Screen):

    def __init__(self, app_state, **kwargs):

        super().__init__(**kwargs)

        self.app_state = app_state

        self.drawer_open = False

        self.drawer = None

        self.drawer_width = dp(285)

        self.content_area = None

        self.welcome_label = None

        self.role_label = None

        self._build_ui()


    # =====================================================
    # BUILD UI
    # =====================================================

    def _build_ui(self):

        self.clear_widgets()

        root = FloatLayout()


        with root.canvas.before:

            Color(
                0.035,
                0.09,
                0.14,
                1,
            )

            self.background_rect = RoundedRectangle(
                pos=root.pos,
                size=root.size,
            )


        root.bind(
            pos=lambda obj, value:
            setattr(
                self.background_rect,
                "pos",
                value,
            ),

            size=lambda obj, value:
            setattr(
                self.background_rect,
                "size",
                value,
            ),
        )


        main = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12),
        )


        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            spacing=dp(8),
        )


        menu_button = Button(
            text="☰",
            font_size="28sp",
            font_name=font_name(),
            color=WHITE,
            background_normal="",
            background_color=(
                0.05,
                0.22,
                0.34,
                1,
            ),
            size_hint_x=None,
            width=dp(58),
        )


        menu_button.bind(
            on_release=self.toggle_menu
        )


        header.add_widget(
            menu_button
        )


        title_box = BoxLayout(
            orientation="vertical",
        )


        title_box.add_widget(
            self._label(
                APP_NAME,
                "20sp",
                WHITE,
                True,
                dp(32),
            )
        )


        title_box.add_widget(
            self._label(
                "سامانه هوشمند آموزشی یکپارچه",
                "11sp",
                (
                    0.78,
                    0.86,
                    0.92,
                    1,
                ),
                False,
                dp(22),
            )
        )


        header.add_widget(
            title_box
        )


        main.add_widget(
            header
        )

        # =================================================
        # Welcome Card
        # =================================================

        welcome = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(5),
            size_hint_y=None,
            height=dp(120),
        )


        with welcome.canvas.before:

            Color(
                1,
                1,
                1,
                0.96,
            )

            self.welcome_rect = RoundedRectangle(
                radius=[dp(18)],
            )


        welcome.bind(
            pos=lambda obj, value:
            setattr(
                self.welcome_rect,
                "pos",
                value,
            ),

            size=lambda obj, value:
            setattr(
                self.welcome_rect,
                "size",
                value,
            ),
        )


        self.welcome_label = self._label(
            "خوش آمدید",
            "20sp",
            PRIMARY,
            True,
            dp(42),
        )


        welcome.add_widget(
            self.welcome_label
        )


        self.role_label = self._label(
            "",
            "14sp",
            SECONDARY,
            False,
            dp(30),
        )


        welcome.add_widget(
            self.role_label
        )


        welcome.add_widget(
            self._label(
                SCHOOL_NAME,
                "12sp",
                SECONDARY,
                False,
                dp(25),
            )
        )


        main.add_widget(
            welcome
        )


        # =================================================
        # Content Area
        # =================================================

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
        )


        self.content_area = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[
                dp(4),
                dp(8),
                dp(4),
                dp(20),
            ],
            size_hint_y=None,
        )


        self.content_area.bind(
            minimum_height=
            self.content_area.setter(
                "height"
            )
        )


        scroll.add_widget(
            self.content_area
        )


        main.add_widget(
            scroll
        )


        # =================================================
        # Version
        # =================================================

        main.add_widget(
            self._label(
                f"نسخه {APP_VERSION}",
                "10sp",
                (
                    0.70,
                    0.78,
                    0.84,
                    1,
                ),
                False,
                dp(22),
            )
        )


        root.add_widget(
            main
        )


        # =================================================
        # Drawer
        # =================================================

        self.drawer = self._build_drawer()


        root.add_widget(
            self.drawer
        )


        self.add_widget(
            root
        )


    # =====================================================
    # LABEL HELPER
    # =====================================================

    def _label(
        self,
        text,
        font_size="14sp",
        color=WHITE,
        bold=False,
        height=dp(40),
    ):

        label = Label(
            text=rtl_text(
                str(text)
            ),
            font_name=font_name(),
            font_size=font_size,
            color=color,
            bold=bold,
            halign="right",
            valign="middle",
            size_hint_y=None,
            height=height,
        )


        label.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value,
            )
        )


        return label


    # =====================================================
    # DRAWER
    # =====================================================

    def _build_drawer(self):

        drawer = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=self.drawer_width,
            size_hint_y=1,
            x=-self.drawer_width,
            padding=dp(14),
            spacing=dp(8),
        )


        with drawer.canvas.before:

            Color(
                0.035,
                0.12,
                0.18,
                1,
            )

            self.drawer_rect = RoundedRectangle(
                radius=[dp(12)],
            )


        drawer.bind(
            pos=lambda obj, value:
            setattr(
                self.drawer_rect,
                "pos",
                value,
            ),

            size=lambda obj, value:
            setattr(
                self.drawer_rect,
                "size",
                value,
            ),
        )


        drawer.add_widget(
            self._label(
                APP_NAME,
                "22sp",
                WHITE,
                True,
                dp(44),
            )
        )


        drawer.add_widget(
            self._label(
                SCHOOL_NAME,
                "12sp",
                (
                    0.80,
                    0.88,
                    0.92,
                    1,
                ),
                False,
                dp(45),
            )
        )


        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
        )


        menu_box = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            size_hint_y=None,
        )


        menu_box.bind(
            minimum_height=
            menu_box.setter(
                "height"
            )
        )


        self._populate_menu(
            menu_box
        )


        scroll.add_widget(
            menu_box
        )


        drawer.add_widget(
            scroll
        )


        close_button = Button(
            text=rtl_text(
                "بستن منو"
            ),
            font_name=font_name(),
            font_size="14sp",
            color=WHITE,
            background_normal="",
            background_color=(
                0.20,
                0.25,
                0.30,
                1,
            ),
            size_hint_y=None,
            height=dp(48),
        )


        close_button.bind(
            on_release=self.close_menu
        )


        drawer.add_widget(
            close_button
        )


        return drawer

    # =====================================================
    # POPULATE MENU
    # =====================================================

    def _populate_menu(self, menu_box):

        role = self._get_role()

        items = ROLE_MENUS.get(
            role,
            ROLE_MENUS["manager"]
        )


        for title, route in items:

            button = Button(
                text=rtl_text(title),
                font_name=font_name(),
                font_size="13sp",
                color=WHITE,
                background_normal="",
                background_color=(
                    0.07,
                    0.20,
                    0.28,
                    1,
                ),
                size_hint_y=None,
                height=dp(46),
            )


            button.bind(
                size=lambda obj, value:
                setattr(
                    obj,
                    "text_size",
                    value,
                )
            )


            button.bind(
                on_release=lambda btn, r=route:
                self._menu_selected(r)
            )


            menu_box.add_widget(
                button
            )


    # =====================================================
    # USER HELPERS
    # =====================================================

    def _get_role(self):

        try:

            role = getattr(
                self.app_state,
                "role",
                None
            )


            if callable(role):
                role = role()


            if role:
                return str(role).lower().strip()


        except Exception:
            pass


        return "manager"



    def _get_display_name(self):

        try:

            name = getattr(
                self.app_state,
                "display_name",
                None
            )


            if callable(name):
                name = name()


            if name:
                return str(name)


        except Exception:
            pass


        return "کاربر"



    # =====================================================
    # DRAWER CONTROL
    # =====================================================

    def _open_drawer(self, *args):

        if not self.drawer:
            return


        self.drawer_open = True


        try:

            from kivy.animation import Animation


            Animation(
                x=0,
                duration=0.2,
            ).start(
                self.drawer
            )


        except Exception:

            self.drawer.x = 0



    def _close_drawer(self, *args):

        if not self.drawer:
            return


        self.drawer_open = False


        try:

            from kivy.animation import Animation


            Animation(
                x=-self.drawer_width,
                duration=0.2,
            ).start(
                self.drawer
            )


        except Exception:

            self.drawer.x = -self.drawer_width



    def _toggle_drawer(self, *args):

        if self.drawer_open:

            self._close_drawer()

        else:

            self._open_drawer()



    # =====================================================
    # NAVIGATION
    # =====================================================

    def _menu_selected(self, route):

        try:

            self._close_drawer()


            if not self.manager:
                return


            if not self.manager.has_screen(
                "module"
            ):

                return


            module = self.manager.get_screen(
                "module"
            )


            if hasattr(
                module,
                "set_module"
            ):

                module.set_module(
                    route
                )


            self.manager.current = "module"



        except Exception as exc:

            print(
                "Dashboard navigation error:",
                exc
            )



    # =====================================================
    # DASHBOARD CONTENT
    # =====================================================

    def _update_welcome(self):

        name = self._get_display_name()

        role = self._get_role()


        title = ROLE_TITLES.get(
            role,
            "کاربر سامانه"
        )


        if self.welcome_label:

            self.welcome_label.text = rtl_text(
                f"خوش آمدید {name} عزیز"
            )


        if self.role_label:

            self.role_label.text = rtl_text(
                title
            )



    def _show_dashboard_home(self):

        if not self.content_area:
            return


        self.content_area.clear_widgets()


        self.content_area.add_widget(

            self._label(
                "به سامانه هوشمند آموزشی یکپارچه فراهوش خوش آمدید",
                "18sp",
                PRIMARY,
                True,
                dp(70),
            )

        )


        self.content_area.add_widget(
            self._label(
                "از منوی کناری بخش مورد نظر را انتخاب کنید.",
                "14sp",
                SECONDARY,
                False,
                dp(60),
            )
        )

        status = "بررسی اتصال به سرور..."
        color = SECONDARY
        try:
            ok, message = self.app_state.check_server() if self.app_state else (False, "برنامه آماده نیست")
            status = ("● " + message) if ok else ("● " + message)
            color = SUCCESS if ok else (1, 0.35, 0.25, 1)
        except Exception as exc:
            status = "● خطا در بررسی اتصال سرور"
            color = (1, 0.35, 0.25, 1)
            print("SERVER STATUS ERROR:", repr(exc))

        self.content_area.add_widget(
            self._label(
                status,
                "14sp",
                color,
                True,
                dp(55),
            )
        )



    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        try:

            self._update_welcome()

            self._show_dashboard_home()


        except Exception as exc:

            print(
                "Dashboard refresh error:",
                exc
            )



    # =====================================================
    # SCREEN EVENTS
    # =====================================================

    def on_enter(self, *args):

        try:

            self.refresh()

            self.drawer_open = False

            if self.drawer:

                self.drawer.x = -self.drawer_width


        except Exception as exc:

            print(
                "Dashboard enter error:",
                exc
            )



    def on_leave(self, *args):

        self._close_drawer()



    # =====================================================
    # LOGOUT
    # =====================================================

    def _logout(self, *args):

        try:

            self._close_drawer()


            if self.app_state:

                if hasattr(
                    self.app_state,
                    "logout"
                ):

                    self.app_state.logout()



            if self.manager and self.manager.has_screen(
                "login"
            ):

                self.manager.current = "login"



        except Exception as exc:

            print(
                "Logout error:",
                exc
            )



    # =====================================================
    # PUBLIC MENU API
    # =====================================================

    def open_menu(self):

        self._open_drawer()



    def close_menu(self):

        self._close_drawer()



    def toggle_menu(self):

        self._toggle_drawer()



    # =====================================================
    # CLEAR CONTENT
    # =====================================================

    def clear_content(self):

        try:

            if self.content_area:

                self.content_area.clear_widgets()


        except Exception as exc:

            print(
                "Clear content error:",
                exc
            )
