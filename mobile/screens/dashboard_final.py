from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

from mobile.config import APP_NAME, SCHOOL_NAME, APP_VERSION, PRIMARY, SECONDARY, SUCCESS, ERROR, WHITE
from mobile.ui import font_name, rtl_text

ROLE_TITLES = {
    "manager": "مدیریت مدرسه", "admin": "مدیریت مدرسه", "principal": "مدیریت مدرسه",
    "educational": "معاون آموزشی", "education": "معاون آموزشی", "assistant_education": "معاون آموزشی",
    "executive": "معاون اجرایی", "assistant_executive": "معاون اجرایی",
    "cultural": "معاون پرورشی", "assistant_cultural": "معاون پرورشی", "training": "معاون پرورشی",
    "advisor": "مشاوره", "counselor": "مشاوره", "teacher": "دبیر", "teachers": "دبیران",
    "student": "دانش‌آموز", "students": "دانش‌آموزان", "parent": "ولی دانش‌آموز", "parents": "اولیا",
}

ROLE_MENUS = {
    "manager": [("🏫 مدیریت مدرسه", "management"), ("📚 معاون آموزشی", "educational"), ("🗂 معاون اجرایی", "executive"), ("🎯 معاون پرورشی", "cultural"), ("👥 دبیران", "teachers"), ("👨‍🎓 دانش‌آموزان", "students"), ("👨‍👩‍👦 اولیا", "parents"), ("💰 امور مالی", "finance"), ("💻 کلاس‌های آنلاین", "online"), ("🖥 تابلو هوشمند", "smart_board"), ("🤖 هوش مصنوعی", "ai"), ("📊 گزارش‌ها", "reports"), ("💬 پیام‌ها", "messages"), ("⚙️ تنظیمات", "settings"), ("📅 برنامه هفتگی", "schedule"), ("ℹ️ درباره فراهوش", "about")],
    "admin": [("🏫 مدیریت مدرسه", "management"), ("👥 دبیران", "teachers"), ("👨‍🎓 دانش‌آموزان", "students"), ("👨‍👩‍👦 اولیا", "parents"), ("💰 امور مالی", "finance"), ("💻 کلاس‌های آنلاین", "online"), ("🖥 تابلو هوشمند", "smart_board"), ("🤖 هوش مصنوعی", "ai"), ("📊 گزارش‌ها", "reports"), ("⚙️ تنظیمات", "settings")],
    "educational": [("📚 معاون آموزشی", "educational"), ("👨‍🎓 دانش‌آموزان", "students"), ("👥 دبیران", "teachers"), ("📅 برنامه هفتگی", "schedule"), ("📊 وضعیت تحصیلی", "student_info"), ("📈 گزارش‌ها", "reports"), ("💻 کلاس‌های آنلاین", "online")],
    "executive": [("🗂 معاون اجرایی", "executive"), ("👨‍🎓 دانش‌آموزان", "students"), ("👨‍👩‍👦 اولیا", "parents"), ("💰 امور مالی", "finance"), ("📊 گزارش‌ها", "reports"), ("⚙️ تنظیمات", "settings")],
    "cultural": [("🎯 معاون پرورشی", "cultural"), ("👨‍🎓 دانش‌آموزان", "students"), ("🖥 تابلو هوشمند", "smart_board"), ("💬 پیام‌ها", "messages"), ("📊 گزارش‌ها", "reports")],
    "teacher": [("👨‍🏫 پنل دبیر", "teacher"), ("📅 برنامه هفتگی", "schedule"), ("👨‍🎓 دانش‌آموزان", "students"), ("💻 کلاس‌های آنلاین", "online"), ("📊 گزارش‌ها", "reports"), ("💬 پیام‌ها", "messages")],
    "student": [("👨‍🎓 پنل دانش‌آموز", "student"), ("📅 برنامه هفتگی", "schedule"), ("📊 وضعیت تحصیلی", "student_info"), ("💻 کلاس آنلاین", "online"), ("💬 پیام‌ها", "messages")],
    "parent": [("👨‍👩‍👦 پنل اولیا", "parent"), ("📊 وضعیت تحصیلی", "student_info"), ("💳 پرداخت‌ها", "payment"), ("💻 کلاس آنلاین", "online"), ("💬 پیام‌ها", "messages")],
}

class DashboardScreen(Screen):
    def __init__(self, app_state, **kwargs):
        super().__init__(**kwargs)
        self.app_state = app_state
        self.drawer_open = False
        self.drawer = None
        self.content_area = None
        self.welcome_label = None
        self.role_label = None
        self._build()

    def _label(self, text, size="14sp", color=WHITE, bold=False, height=dp(44)):
        label = Label(text=rtl_text(str(text)), font_name=font_name(), font_size=size, color=color, bold=bold, halign="right", valign="middle", size_hint_y=None, height=height)
        label.bind(size=lambda obj, value: setattr(obj, "text_size", value))
        return label

    def _get_role(self):
        try:
            role = getattr(self.app_state, "role", "manager") or "manager"
            return str(role).lower().strip()
        except Exception:
            return "manager"

    def _get_name(self):
        try:
            return str(getattr(self.app_state, "display_name", "کاربر") or "کاربر")
        except Exception:
            return "کاربر"

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        header = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(8))
        menu = Button(text="☰", font_name=font_name(), font_size="28sp", color=WHITE, background_normal="", background_color=PRIMARY, size_hint_x=None, width=dp(58))
        menu.bind(on_release=self.toggle_menu)
        header.add_widget(menu)
        header.add_widget(self._label(APP_NAME, "21sp", WHITE, True, dp(50)))
        root.add_widget(header)

        welcome = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(2), size_hint_y=None, height=dp(112))
        self.welcome_label = self._label("خوش آمدید", "20sp", PRIMARY, True, dp(45))
        self.role_label = self._label("", "14sp", SECONDARY, False, dp(32))
        welcome.add_widget(self.welcome_label)
        welcome.add_widget(self.role_label)
        welcome.add_widget(self._label(SCHOOL_NAME, "12sp", SECONDARY, False, dp(25)))
        root.add_widget(welcome)

        scroll = ScrollView(do_scroll_x=False)
        self.content_area = BoxLayout(orientation="vertical", spacing=dp(8), padding=[dp(4), dp(6), dp(4), dp(18)], size_hint_y=None)
        self.content_area.bind(minimum_height=self.content_area.setter("height"))
        scroll.add_widget(self.content_area)
        root.add_widget(scroll)
        root.add_widget(self._label(f"نسخه {APP_VERSION}", "10sp", SECONDARY, False, dp(20)))
        self.add_widget(root)
        self.drawer = self._build_drawer()
        root.add_widget(self.drawer)

    def _build_drawer(self):
        drawer = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(6), size_hint_x=None, width=dp(285), x=-dp(285))
        drawer.add_widget(self._label(APP_NAME, "22sp", WHITE, True, dp(45)))
        drawer.add_widget(self._label(SCHOOL_NAME, "12sp", SECONDARY, False, dp(35)))
        scroll = ScrollView(do_scroll_x=False)
        box = BoxLayout(orientation="vertical", spacing=dp(6), size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        self._populate_menu(box)
        scroll.add_widget(box)
        drawer.add_widget(scroll)
        close = Button(text=rtl_text("بستن منو"), font_name=font_name(), size_hint_y=None, height=dp(46), background_normal="", background_color=PRIMARY, color=WHITE)
        close.bind(on_release=self.close_menu)
        drawer.add_widget(close)
        return drawer

    def _populate_menu(self, box):
        items = ROLE_MENUS.get(self._get_role(), ROLE_MENUS["manager"])
        for title, route in items:
            btn = Button(text=rtl_text(title), font_name=font_name(), font_size="13sp", color=WHITE, background_normal="", background_color=(0.07, 0.20, 0.28, 1), size_hint_y=None, height=dp(46))
            btn.bind(on_release=lambda _btn, r=route: self._menu_selected(r))
            box.add_widget(btn)

    def toggle_menu(self, *_):
        if self.drawer_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self, *_):
        self.drawer_open = True
        try:
            from kivy.animation import Animation
            Animation(x=0, duration=.18).start(self.drawer)
        except Exception:
            self.drawer.x = 0

    def close_menu(self, *_):
        self.drawer_open = False
        try:
            from kivy.animation import Animation
            Animation(x=-dp(285), duration=.18).start(self.drawer)
        except Exception:
            self.drawer.x = -dp(285)

    def _menu_selected(self, route):
        self.close_menu()
        try:
            if self.manager and self.manager.has_screen("module"):
                module = self.manager.get_screen("module")
                setter = getattr(module, "set_module", None)
                if callable(setter): setter(route)
                else:
                    refresher = getattr(module, "refresh", None)
                    if callable(refresher): refresher(route)
                self.manager.current = "module"
        except Exception as exc:
            print("DASHBOARD NAVIGATION ERROR:", repr(exc))

    def _show_home(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self._label("به سامانه هوشمند آموزشی یکپارچه فراهوش خوش آمدید", "17sp", PRIMARY, True, dp(64)))
        self.content_area.add_widget(self._label("از منوی بالا بخش مورد نظر را انتخاب کنید.", "14sp", SECONDARY, False, dp(50)))
        try:
            ok, message = self.app_state.check_server() if self.app_state else (False, "برنامه آماده نیست")
            self.content_area.add_widget(self._label("● " + message, "14sp", SUCCESS if ok else ERROR, True, dp(50)))
        except Exception as exc:
            print("SERVER STATUS ERROR:", repr(exc))
            self.content_area.add_widget(self._label("● وضعیت اتصال قابل بررسی نیست", "14sp", ERROR, True, dp(50)))

    def refresh(self):
        self.welcome_label.text = rtl_text(f"خوش آمدید {self._get_name()} عزیز")
        self.role_label.text = rtl_text(ROLE_TITLES.get(self._get_role(), "کاربر سامانه"))
        self._show_home()

    def on_pre_enter(self, *args):
        self.refresh()
        return super().on_pre_enter(*args)
