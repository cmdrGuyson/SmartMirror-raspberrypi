from kivy.app import App
from kivy.core.window import Window
from kivy.loader import Loader
from kivy.uix.screenmanager import ScreenManager
from imutils.video import VideoStream

import time

# Import Views and Screens
from main_window import MainWindow
from news_rv import News_RV, NewsRow
from idle_window import IdleWindow
from tweets_rv import Tweets_RV

# Run app in fullscreen
Window.fullscreen = "auto"


class WindowManager(ScreenManager):
    pass


class MainWindowApp(App):
    def build(self):
        Loader.loading_image = 'images/loading.zip'
        sm = WindowManager()
        self.stream = VideoStream(src=0).start()
        time.sleep(2.0)

        sm.add_widget(IdleWindow(self.stream, name='idle'))
        sm.add_widget(MainWindow(self.stream, name='main'))

        return sm


if __name__ == "__main__":
    MainWindowApp().run()
