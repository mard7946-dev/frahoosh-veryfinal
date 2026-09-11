from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from mobile.config import APP_NAME, BACKGROUND
from mobile.ui import register_fonts
from mobile.services.app_state import AppState


class FrahooshMobileApp(App):
    title = APP_NAME

    def build(self):
        Window.clearcolor = BACKGROUND
        register_fonts()

        try:
            self.state = AppState()
        except Exception as exc:
            print("APP STATE INIT ERROR:", repr(exc))
            self.state = None

        manager = ScreenManager(transition=FadeTransition(duration=.15))
        self._add(manager, "mobile.screens.login", "LoginScreen", "login")
        self._add(manager, "mobile.screens.dashboard", "DashboardScreen", "dashboard")
        self._add(manager, "mobile.screens.module", "ModuleScreen", "module")
        self._add(manager, "mobile.screens.update", "UpdateScreen", "update")
        self._add(manager, "mobile.screens.loading", "LoadingScreen", "loading")

        manager.current = "loading" if manager.has_screen("loading") else "login"
        Clock.schedule_once(lambda *_: print("FRAHOOSH READY", manager.screen_names), 0)
        return manager

    def _add(self, manager, module_path, class_name, screen_name):
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            manager.add_widget(cls(self.state, name=screen_name))
            print(screen_name.upper(), "SCREEN READY")
        except Exception as exc:
            import traceback
            traceback.print_exc()
            print(screen_name.upper(), "LOAD ERROR:", repr(exc))


if __name__ == "__main__":
    FrahooshMobileApp().run()
