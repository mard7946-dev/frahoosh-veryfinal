from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.clock import Clock
from mobile.ui import register_fonts


class FrahooshMobileApp(App):
    title = "فراهوش"

    def build(self):
        Window.clearcolor = (0.965, 0.975, 0.985, 1)
        print("FRAHOOSH START")

        try:
            register_fonts()
            print("FONT READY")
        except Exception as exc:
            print("FONT REGISTER ERROR:", repr(exc))

        self.state = None
        try:
            from mobile.services.app_state import AppState
            self.state = AppState()
            print("APP STATE READY")
        except Exception as exc:
            print("APP STATE ERROR:", repr(exc))

        manager = ScreenManager(transition=FadeTransition(duration=0.15))

        def add_screen(screen_class, module_path, screen_name):
            try:
                module = __import__(module_path, fromlist=[screen_class])
                cls = getattr(module, screen_class)
                screen = cls(self.state, name=screen_name)
                manager.add_widget(screen)
                print(screen_name.upper(), "SCREEN READY")
                return True
            except Exception as exc:
                import traceback
                traceback.print_exc()
                print(screen_name.upper(), "LOAD ERROR:", type(exc).__name__, str(exc))
                return False

        add_screen("LoadingScreen", "mobile.screens.loading", "loading")
        add_screen("LoginScreen", "mobile.screens.login", "login")
        add_screen("DashboardScreen", "mobile.screens.dashboard_final", "dashboard")
        add_screen("ModuleScreen", "mobile.screens.module", "module")
        add_screen("UpdateScreen", "mobile.screens.update", "update")

        if manager.has_screen("loading"):
            manager.current = "loading"
        elif manager.has_screen("login"):
            manager.current = "login"
        elif manager.screen_names:
            manager.current = manager.screen_names[0]

        print("AVAILABLE SCREENS:", manager.screen_names)
        Clock.schedule_once(lambda dt: print("FRAHOOSH READY"), 1)
        return manager


if __name__ == "__main__":
    FrahooshMobileApp().run()
