from threading import Thread

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.metrics import dp

from mobile.config import (
    APP_NAME,
    SYSTEM_TITLE,
    LOGO_PATH,
    PRIMARY,
    SECONDARY,
    BACKGROUND,
)

from mobile.ui import (
    font_name,
    rtl_text,
)


class LoadingScreen(Screen):

    def __init__(
        self,
        app_state,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.app_state = app_state
        self._finished = False
        self._worker_started = False

        self.add_widget(
            self._build()
        )

        # ---------------------------------------------
        # حداکثر زمان Loading
        # ---------------------------------------------

        Clock.schedule_once(
            self._start_auth_check,
            0.40
        )

        Clock.schedule_once(
            self._loading_timeout,
            8.0
        )

    # ========================================================
    # UI
    # ========================================================

    def _build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(28),
            spacing=dp(12)
        )

        root.add_widget(
            BoxLayout(
                size_hint_y=0.20
            )
        )

        try:

            from pathlib import Path

            if Path(
                LOGO_PATH
            ).exists():

                root.add_widget(
                    Image(
                        source=LOGO_PATH,
                        size_hint_y=None,
                        height=dp(150),
                        allow_stretch=True,
                        keep_ratio=True
                    )
                )

        except Exception:
            pass

        root.add_widget(
            Label(
                text=rtl_text(
                    APP_NAME
                ),
                font_name=font_name(),
                font_size="34sp",
                bold=True,
                color=PRIMARY,
                size_hint_y=None,
                height=dp(60)
            )
        )

        root.add_widget(
            Label(
                text=rtl_text(
                    SYSTEM_TITLE
                ),
                font_name=font_name(),
                font_size="16sp",
                color=SECONDARY,
                size_hint_y=None,
                height=dp(45)
            )
        )

        self.status = Label(
            text=rtl_text(
                "در حال آماده‌سازی برنامه..."
            ),
            font_name=font_name(),
            font_size="13sp",
            color=SECONDARY,
            size_hint_y=None,
            height=dp(36)
        )

        root.add_widget(
            self.status
        )

        root.add_widget(
            BoxLayout(
                size_hint_y=0.45
            )
        )

        return root

    # ========================================================
    # Authentication
    # ========================================================

    def _start_auth_check(self, *_):

        if self._finished:
            return

        if self._worker_started:
            return

        self._worker_started = True

        try:

            self.status.text = rtl_text(
                "در حال بررسی نشست کاربر..."
            )

        except Exception:
            pass

        Thread(
            target=self._auth_worker,
            daemon=True
        ).start()

    # ========================================================
    # Worker
    # ========================================================

    def _auth_worker(self):

        try:

            state = self.app_state

            if state is None:

                self._schedule_login()
                return

            # ------------------------------------------------
            # هیچ Session معتبری وجود ندارد
            # ------------------------------------------------

            if not state.logged_in:

                self._schedule_login()
                return

            # ------------------------------------------------
            # Server must be reachable before opening the app.
            # ------------------------------------------------
            ok, message = state.check_server()
            if not ok:
                self.status.text = rtl_text(message)
                self._schedule_login()
                return

            # ------------------------------------------------
            # Refresh first, then validate the access token.
            # ------------------------------------------------
            refreshed = False
            try:
                refreshed = bool(state.refresh_session())
            except Exception:
                refreshed = False

            if refreshed or state.validate_server_session():
                self._schedule_dashboard()
                return

            self._schedule_login()

        except Exception:

            self._schedule_login()

    # ========================================================
    # Timeout
    # ========================================================

    def _loading_timeout(self, *_):

        if self._finished:
            return

        self._schedule_login()

    # ========================================================
    # Navigation Helpers
    # ========================================================

    def _schedule_login(self):

        Clock.schedule_once(
            lambda dt: self._go_login(),
            0
        )

    def _schedule_dashboard(self):

        Clock.schedule_once(
            lambda dt: self._go_dashboard(),
            0
        )

    # ========================================================
    # Dashboard
    # ========================================================

    def _go_dashboard(self):

        if self._finished:
            return

        try:

            if self.manager is None:
                return

            self._finished = True

            self.manager.current = (
                "dashboard"
            )

        except Exception:

            self._finished = False

            self._go_login()

    # ========================================================
    # Login
    # ========================================================

    def _go_login(self):

        if self._finished:
            return

        try:

            if self.manager is None:
                return

            self._finished = True

            self.manager.current = (
                "login"
            )

        except Exception:
            self._finished = True                  
                    
