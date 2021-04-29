from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class IdleWindow(Screen):
    pass


class LoggedWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("idle.kv")


class IdleApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    IdleApp().run()
