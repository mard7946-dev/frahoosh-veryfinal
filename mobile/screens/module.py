from threading import Thread

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from mobile.config import (
    APP_NAME,
    SCHOOL_NAME,
    SCHOOL_YEAR,
    PRIMARY,
    SECONDARY,
    SUCCESS,
    ERROR,
    WHITE,
)

from mobile.ui import (
    font_name,
    rtl_text,
)


MODULE_TITLES = {

    "management": "مدیریت",
    "educational": "معاون آموزشی",
    "executive": "معاون اجرایی",
    "cultural": "معاون پرورشی",
    "advisor": "مشاوره",

    "teacher": "پنل دبیر",
    "teachers": "دبیران",

    "student": "پنل دانش‌آموز",
    "students": "دانش‌آموزان",

    "parent": "پنل اولیا",
    "parents": "اولیا",

    "finance": "مالی",
    "payment": "پرداخت آنلاین",

    "online": "کلاس‌های آنلاین",

    "smart_board": "تابلو هوشمند",

    "ai": "دستیار هوش مصنوعی",

    "messages": "صندوق پیام‌ها",

    "settings": "تنظیمات",

    "reports": "گزارش‌ها",

    "schedule": "برنامه هفتگی",

    "student_info": "وضعیت تحصیلی",
}



MODULE_TABLES = {
    "settings": ["account_settings"],
}

SUBPANELS = {
    "management": ["اطلاعات مدرسه", "کاربران و نقش‌ها", "تنظیمات سامانه", "گزارش مدیریتی"],
    "educational": ["کلاس‌ها و دروس", "برنامه هفتگی", "نمرات و ارزشیابی", "گزارش افت تحصیلی"],
    "executive": ["ثبت‌نام دانش‌آموزان", "پرونده دانش‌آموز", "امور مالی", "گزارش‌های اجرایی"],
    "cultural": ["فعالیت‌های پرورشی", "جشنواره‌ها و مسابقات", "عملکرد دانش‌آموز", "اطلاعیه‌های فرهنگی"],
    "advisor": ["مشاوره دانش‌آموز", "پیگیری وضعیت", "گزارش مشاوره"],
    "teacher": ["کلاس‌های من", "ثبت نمره", "حضور و غیاب", "تکالیف و طرح درس", "کلاس آنلاین"],
    "teachers": ["فهرست دبیران", "کلاس‌های دبیران", "گزارش عملکرد"],
    "student": ["درس‌ها و دبیران", "برنامه هفتگی", "نمرات", "تکالیف", "کلاس آنلاین"],
    "students": ["فهرست دانش‌آموزان", "کلاس‌ها", "وضعیت تحصیلی", "گزارش‌ها"],
    "parent": ["وضعیت تحصیلی فرزند", "غیبت‌ها", "پرداخت‌ها", "پیام‌های مدرسه", "کلاس آنلاین"],
    "parents": ["فهرست اولیا", "فرزندان", "پرداخت‌ها", "پیام‌ها"],
    "finance": ["پرداخت‌ها", "بدهی‌ها", "رسیدها", "گزارش مالی"],
    "payment": ["پرداخت جدید", "سوابق پرداخت", "رسیدها"],
    "online": ["کلاس‌های فعال", "کلاس‌های آینده", "حضور و غیاب آنلاین", "فایل و تکلیف", "گفت‌وگو"],
    "smart_board": ["فایل‌های آموزشی", "تصویر و ویدئو", "آزمون کوتاه", "محتوای کلاس"],
    "ai": ["دستیار هوشمند", "تحلیل آموزشی", "گزارش هوشمند", "پرسش و پاسخ"],
    "messages": ["پیام‌های دریافتی", "ارسال پیام", "اطلاعیه‌های مدرسه"],
    "settings": ["تنظیمات حساب", "تنظیمات مدرسه", "سال تحصیلی", "اتصال سرور"],
    "reports": ["گزارش دانش‌آموز", "گزارش کلاس", "گزارش دبیر", "گزارش مدیریتی"],
    "schedule": ["برنامه هفتگی", "کلاس‌های امروز", "کلاس‌های آینده"],
    "student_info": ["نمرات", "حضور و غیاب", "روند تحصیلی", "گزارش وضعیت"],
}



class ModuleScreen(Screen):


    def __init__(
        self,
        app_state,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.app_state = app_state

        self.module_key = ""

        self.loading_label = None

        self._build()



    # ============================
    # UI
    # ============================


    def _build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(10),
        )


        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            spacing=dp(8),
        )


        self.back_button = Button(
            text=rtl_text(
                "‹ داشبورد"
            ),
            font_name=font_name(),
            font_size="14sp",
            background_normal="",
            background_color=PRIMARY,
            color=WHITE,
            size_hint_x=None,
            width=dp(110),
        )


        self.back_button.bind(
            on_release=self.go_back
        )


        header.add_widget(
            self.back_button
        )


        self.title_label = Label(
            text="",
            font_name=font_name(),
            font_size="20sp",
            color=PRIMARY,
            bold=True,
            halign="right",
            valign="middle",
        )


        self.title_label.bind(
            size=self._sync_text
        )


        header.add_widget(
            self.title_label
        )


        root.add_widget(
            header
        )


        self.content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
        )


        self.scroll = ScrollView()


        self.body = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
        )


        self.body.bind(
            minimum_height=self.body.setter(
                "height"
            )
        )


        self.scroll.add_widget(
            self.body
        )


        self.content.add_widget(
            self.scroll
        )


        root.add_widget(
            self.content
        )


        self.add_widget(
            root
        )

    # ============================
    # REFRESH
    # ============================

    def refresh(
        self,
        module_key=None
    ):

        if module_key:

            self.module_key = (
                module_key
            )


        title = MODULE_TITLES.get(
            self.module_key,
            "بخش فراهوش"
        )


        self.title_label.text = rtl_text(
            title
        )


        self.body.clear_widgets()


        self._show_loading()



        Thread(
            target=self._load_module_data,
            daemon=True
        ).start()



    # ============================
    # LOAD DATA
    # ============================


    def _load_module_data(self):

        try:

            data = {

                "title":
                    MODULE_TITLES.get(
                        self.module_key,
                        "بخش فراهوش"
                    ),

                "items":
                    self._get_module_items()

            }


            Clock.schedule_once(

                lambda dt:
                self._render_module(
                    data
                )

            )


        except Exception as exc:

            print(
                "MODULE LOAD ERROR:",
                repr(exc)
            )


            Clock.schedule_once(

                lambda dt:
                self._show_error(
                    str(exc)
                )

            )



    def _get_module_items(self):

        items = []


        tables = MODULE_TABLES.get(

            self.module_key,

            []

        )


        if self.app_state is None:

            return items



        if self.app_state.api is None:

            return items



        for table in tables:

            try:

                rows = (
                    self.app_state.api.table_select(
                        table
                    )
                )


                if isinstance(
                    rows,
                    list
                ):

                    items.extend(
                        rows
                    )


            except Exception as exc:

                print(

                    "TABLE LOAD ERROR",
                    table,
                    repr(exc)

                )



        return items



    # ============================
    # RENDER
    # ============================


    def _render_module(
        self,
        data
    ):


        self.body.clear_widgets()


        items = (

            data.get(
                "items"
            )

            or []

        )


        backend_ok = bool(
            self.app_state
            and self.app_state.api
            and self.app_state.api.configured
            and self.app_state.api.access_token
        )

        if items:
            for item in items:
                self.body.add_widget(self._create_card(item))
            return

        status = (
            "اتصال سرور و نشست کاربر برقرار است."
            if backend_ok
            else "اتصال سرور/نشست هنوز برقرار نشده است."
        )
        status_color = SUCCESS if backend_ok else ERROR
        self.body.add_widget(Label(
            text=rtl_text(status), font_name=font_name(), font_size="14sp",
            color=status_color, halign="right", valign="middle",
            size_hint_y=None, height=dp(42)))

        # Every route has a concrete visible sub-panel structure. We never
        # invent database rows; real rows are rendered only from known APIs.
        for subtitle in SUBPANELS.get(self.module_key, ["داشبورد بخش"]):
            card = BoxLayout(
                orientation="vertical", padding=dp(12), spacing=dp(4),
                size_hint_y=None, height=dp(82)
            )
            card.add_widget(Label(
                text=rtl_text(subtitle), font_name=font_name(),
                font_size="15sp", color=PRIMARY, bold=True,
                halign="right", valign="middle"
            ))
            card.add_widget(Label(
                text=rtl_text(
                    "آماده اتصال به داده‌های واقعی سامانه"
                    if backend_ok else "نیازمند اتصال معتبر به سرور"
                ),
                font_name=font_name(), font_size="11sp", color=SECONDARY,
                halign="right", valign="middle"
            ))
            self.body.add_widget(card)


    def _create_card(
        self,
        item
    ):


        box = BoxLayout(

            orientation="vertical",

            padding=dp(12),

            spacing=dp(6),

            size_hint_y=None,

            height=dp(100),

        )


        if not isinstance(
            item,
            dict
        ):

            item = {

                "value":
                    str(item)

            }



        title = (

            item.get(
                "title"
            )

            or item.get(
                "name"
            )

            or item.get(
                "full_name"
            )

            or item.get(
                "value"
            )

            or "-"

        )


        label = Label(

            text=rtl_text(

                str(title)

            ),

            font_name=font_name(),

            font_size="15sp",

            color=PRIMARY,

            halign="right",

            valign="middle",

        )


        label.bind(

            size=self._sync_text

        )


        box.add_widget(
            label
        )



        details = []


        for key, value in item.items():


            if key in (
                "id",
                "created_at",
                "updated_at",
            ):

                continue



            if value:

                details.append(

                    f"{key}: {value}"

                )



        if details:


            info = Label(

                text=rtl_text(

                    "\n".join(

                        details[:3]

                    )

                ),

                font_name=font_name(),

                font_size="12sp",

                color=SECONDARY,

                halign="right",

                valign="middle",

            )


            info.bind(

                size=self._sync_text

            )


            box.add_widget(

                info

            )



        return box

    # ============================
    # LOADING / ERROR
    # ============================


    def _show_loading(self):

        self.body.clear_widgets()


        self.loading_label = Label(

            text=rtl_text(

                "در حال بارگذاری اطلاعات..."

            ),

            font_name=font_name(),

            font_size="16sp",

            color=SECONDARY,

            size_hint_y=None,

            height=dp(70),

        )


        self.body.add_widget(

            self.loading_label

        )



    def _show_error(
        self,
        message
    ):


        self.body.clear_widgets()


        label = Label(

            text=rtl_text(

                "خطا در دریافت اطلاعات\n"

                + str(message)

            ),

            font_name=font_name(),

            font_size="14sp",

            color=ERROR,

            halign="center",

            valign="middle",

            size_hint_y=None,

            height=dp(100),

        )


        label.bind(

            size=self._sync_text

        )


        self.body.add_widget(

            label

        )



    # ============================
    # NAVIGATION
    # ============================


    def go_back(
        self,
        *_ 
    ):

        try:

            if self.manager and self.manager.has_screen(
                "dashboard"
            ):

                self.manager.current = (
                    "dashboard"
                )


        except Exception as exc:

            print(

                "BACK ERROR:",

                repr(exc)

            )



    def _menu_open(
        self,
        route
    ):

        self.module_key = route

        self.refresh()



    # ============================
    # SCREEN EVENTS
    # ============================


    def on_pre_enter(
        self,
        *args
    ):

        return super().on_pre_enter(
            *args
        )



    def on_enter(
        self,
        *args
    ):

        try:

            if not self.module_key:

                self.module_key = (
                    "management"
                )


            self.refresh()


        except Exception as exc:

            print(

                "MODULE ENTER ERROR:",

                repr(exc)

            )


        return super().on_enter(
            *args
        )



    # ============================
    # HELPERS
    # ============================


    def _sync_text(
        self,
        obj,
        value
    ):

        obj.text_size = value



    def get_title(self):

        return MODULE_TITLES.get(

            self.module_key,

            APP_NAME

        )



    def set_module(
        self,
        module_key
    ):

        self.module_key = (

            module_key

            or ""

        )


        self.refresh()



    def clear(self):

        self.body.clear_widgets()

        self.module_key = ""



