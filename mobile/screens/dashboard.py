from kivy.animation import Animation
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
    "manager": [("مدیریت مدرسه", "management"), ("معاون آموزشی", "educational"), ("معاون اجرایی", "executive"), ("معاون پرورشی", "cultural"), ("مشاوره", "advisor"), ("دبیران", "teachers"), ("دانش‌آموزان", "students"), ("اولیا", "parents"), ("مالی", "finance"), ("پرداخت آنلاین", "payment"), ("کلاس‌های آنلاین", "online"), ("تابلو هوشمند", "smart_board"), ("دستیار هوش مصنوعی", "ai"), ("گزارش‌ها", "reports"), ("صندوق پیام‌ها", "messages"), ("تنظیمات", "settings"), ("درباره برنامه", "about")],
    "executive": [("معاون اجرایی", "executive"), ("دانش‌آموزان", "students"), ("اولیا", "parents"), ("مالی", "finance"), ("پیام‌ها", "messages"), ("تنظیمات", "settings")],
    "educational": [("معاون آموزشی", "educational"), ("دانش‌آموزان", "students"), ("دبیران", "teachers"), ("برنامه هفتگی", "schedule"), ("کلاس‌های آنلاین", "online"), ("گزارش‌ها", "reports")],
    "cultural": [("معاون پرورشی", "cultural"), ("دانش‌آموزان", "students"), ("فعالیت‌های فرهنگی", "cultural_activity"), ("پیام‌ها", "messages"), ("گزارش‌ها", "reports")],
    "advisor": [("مشاوره", "advisor"), ("پرونده دانش‌آموزان", "students"), ("گزارش مشاوره", "reports"), ("پیام‌ها", "messages")],
    "teacher": [("کلاس‌های من", "my_classes"), ("دانش‌آموزان", "students"), ("حضور و غیاب", "attendance"), ("نمرات", "grades"), ("تکالیف", "homework"), ("کلاس آنلاین", "online"), ("پیام‌ها", "messages")],
    "student": [("کلاس‌های من", "my_classes"), ("برنامه هفتگی", "schedule"), ("نمرات", "grades"), ("تکالیف", "homework"), ("کلاس آنلاین", "online"), ("پیام‌ها", "messages")],
    "parent": [("فرزند من", "children"), ("حضور و غیاب", "attendance"), ("نمرات", "grades"), ("پرداخت‌ها", "payment"), ("پیام‌ها", "messages")],
}


class DashboardScreen(Screen):
    def __init__(self, app_state=None, **kwargs):
        super().__init__(**kwargs)
        self.app_state = app_state
        self.drawer = None
        self.content_area = None
        self.welcome_label = None
        self.role_label = None
        self._build()

    def _label(self, text, size="14sp", color=WHITE, bold=False, height=dp(44)):
        label = Label(text=rtl_text(str(text)), font_name=font_name(), font_size=size, color=color, bold=bold, halign="right", valign="middle", size_hint_y=None, height=height)
        label.bind(size=lambda obj, value: setattr(obj, "text_size", value))
        return label

    def _role(self):
        return str(getattr(self.app_state, "role", "student") or "student").lower().strip()

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        header = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(8))
        menu = Button(text="☰", font_name=font_name(), font_size="28sp", color=WHITE, background_normal="", background_color=PRIMARY, size_hint_x=None, width=dp(58))
        menu.bind(on_release=self.toggle_menu)
        header.add_widget(menu)
        header.add_widget(self._label(APP_NAME, "21sp", WHITE, True, dp(50)))
        root.add_widget(header)
        welcome = BoxLayout(orientation="vertical", padding=dp(10), size_hint_y=None, height=dp(105))
        self.welcome_label = self._label("خوش آمدید", "20sp", PRIMARY, True, dp(42))
        self.role_label = self._label("", "14sp", SECONDARY, False, dp(30))
        welcome.add_widget(self.welcome_label)
        welcome.add_widget(self.role_label)
        welcome.add_widget(self._label(SCHOOL_NAME, "11sp", SECONDARY, False, dp(24)))
        root.add_widget(welcome)
        scroll = ScrollView(do_scroll_x=False)
        self.content_area = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8), size_hint_y=None)
        self.content_area.bind(minimum_height=self.content_area.setter("height"))
        scroll.add_widget(self.content_area)
        root.add_widget(scroll)
        root.add_widget(self._label(f"نسخه {APP_VERSION}", "10sp", SECONDARY, False, dp(20)))
        self.add_widget(root)
        self.drawer = self._make_drawer()
        root.add_widget(self.drawer)

    def _make_drawer(self):
        drawer = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(6), size_hint_x=None, width=dp(290), x=-dp(290))
        drawer.add_widget(self._label(APP_NAME, "22sp", WHITE, True, dp(44)))
        box = BoxLayout(orientation="vertical", spacing=dp(6), size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        for title, route in ROLE_MENUS.get(self._role(), ROLE_MENUS["student"]):
            button = Button(text=rtl_text(title), font_name=font_name(), font_size="13sp", color=WHITE, background_normal="", background_color=PRIMARY, size_hint_y=None, height=dp(46))
            button.bind(on_release=lambda _b, r=route: self.open_module(r))
            box.add_widget(button)
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(box)
        drawer.add_widget(scroll)
        logout = Button(text=rtl_text("خروج از حساب"), font_name=font_name(), color=WHITE, background_normal="", background_color=ERROR, size_hint_y=None, height=dp(48))
        logout.bind(on_release=lambda *_: self.logout())
        drawer.add_widget(logout)
        return drawer

    def toggle_menu(self, *_):
        target = 0 if self.drawer.x < 0 else -dp(290)
        Animation(x=target, duration=.18).start(self.drawer)

    def open_module(self, route):
        try:
            if self.manager and self.manager.has_screen("module"):
                module = self.manager.get_screen("module")
                if hasattr(module, "set_module"):
                    module.set_module(route)
                else:
                    module.refresh(route)
                self.manager.current = "module"
        except Exception as exc:
            print("DASHBOARD NAVIGATION ERROR:", repr(exc))

    def refresh(self):
        name = getattr(self.app_state, "display_name", "کاربر") if self.app_state else "کاربر"
        role = self._role()
        self.welcome_label.text = rtl_text(f"خوش آمدید {name} عزیز")
        self.role_label.text = rtl_text(ROLE_TITLES.get(role, "کاربر سامانه"))
        self.content_area.clear_widgets()
        try:
            ok, msg = self.app_state.check_server() if self.app_state else (False, "برنامه آماده نیست")
            color = SUCCESS if ok else ERROR
            self.content_area.add_widget(self._label("● " + msg, "14sp", color, True, dp(50)))
        except Exception as exc:
            self.content_area.add_widget(self._label("● خطا در بررسی اتصال سرور", "14sp", ERROR, True, dp(50)))
            print("SERVER STATUS ERROR:", repr(exc))

    def on_pre_enter(self, *args):
        self.refresh()
        return super().on_pre_enter(*args)

    def logout(self):
        if self.app_state:
            self.app_state.logout()
        if self.manager and self.manager.has_screen("login"):
            self.manager.current = "login"
