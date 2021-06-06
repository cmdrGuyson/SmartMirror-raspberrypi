from kivy.app import App
from kivy.core.window import Window
from kivy.loader import Loader
from kivy.uix.screenmanager import ScreenManager
from imutils.video import VideoStream

import time

# Import Views and Screens
from screens.main_window import MainWindow
from views.news_rv import News_RV, NewsRow
from screens.idle_window import IdleWindow
from views.tweets_rv import Tweets_RV

# Run app in fullscreen
Window.fullscreen = "auto"


class WindowManager(ScreenManager):
    pass


class MainWindowApp(App):
    def build(self):
        Loader.loading_image = 'images/loading.zip'
        sm = WindowManager()

        # Video stream
        self.stream = VideoStream(src=0).start()

        # Video stream for Raspberry pi
        # self.stream = VideoStream(usePiCamera=True).start()

        time.sleep(2.0)

        sm.add_widget(IdleWindow(self.stream, name='idle'))
        sm.add_widget(MainWindow(self.stream, name='main'))

        return sm


if __name__ == "__main__":
    MainWindowApp().run()
