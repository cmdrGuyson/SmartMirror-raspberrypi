from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.loader import Loader
from kivy.clock import Clock
from utils import StringUtils
from kivy.uix.screenmanager import ScreenManager, Screen
import datetime
from datetime import date

# Run app in fullscreen
Window.fullscreen = "auto"

# Window.maximize()

# Dummy news data
news_data = [{"title": "Dow Tumbles, But GME Stock Rockets 113%; Bitcoin Surges, As Elon Musk Updates Twitter Bio",
              "description": "The Dow Jones Industrial Average dived 400 points Friday, as the price of Bitcoin "
                             "surged 15% on Tesla CEO Elon Musk's Twitter bio change. GME stock soared."},
             {"title": "SoftBank's Son expects mass production of driverless cars in two years - Reuters",
              "description": "SoftBank Group Corp Chief Executive Masayoshi Son said on Friday he expects mass "
                             "production of self-driving vehicles to start in two years."}]

topic = "tesla"
news_api_key = "d49d3a280bd140d7aa43a04f8dab9424"
news_api_url = "https://newsapi.org/v2/top-headlines?language=en&category=entertainment&apiKey=d49d3a280bd140d7aa43a04f8dab9424"

city = "Colombo"
weather_api_key = "45a867178f240b38b171ca8fcc4999a0"
weather_api_url = "http://api.openweathermap.org/data/2.5/weather?q=Colombo&appid=45a867178f240b38b171ca8fcc4999a0&units=metric"

weather = {"main": {"temp": 25.5}, "weather": [{
    "main": "Clouds", "description": "broken clouds"}]}

LOCAL_TIMEZONE = datetime.datetime.now(
    datetime.timezone.utc).astimezone().tzinfo


class IdleWindow(Screen):
    def __init__(self, **kwargs):
        super(IdleWindow, self).__init__(**kwargs)

        self.bool = True

        Clock.schedule_interval(self.change_screen, 5)

    def change_screen(self, t):
        if self.bool is True:
            # self.manager.get_screen('main').set_stuff()
            self.manager.current = "main"


class MainWindow(Screen):
    greeting = ObjectProperty(None)
    date = ObjectProperty(None)
    time = ObjectProperty(None)
    weather_type = ObjectProperty(None)
    temperature = ObjectProperty(None)
    weather_icon = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        Clock.schedule_interval(self.update_time, 1)

    def on_pre_enter(self, **kwargs):
        self.greeting.text = "Hello Amal!"

    def set_stuff(self):
        self.greeting.text = "Hello Chaminda!"
        self.get_weather()

    def get_weather(self):
        # UrlRequest(weather_api_url, on_success=self.update_view,
        #            on_error=self.update_view)
        self.update_view(None, weather)
        pass

    def update_view(self, request, result):
        self.temperature.text = str(result["main"]["temp"]) + "°C"
        self.weather_type.text = result["weather"][0]["description"].title()
        self.weather_icon.source = "images/" + \
            result["weather"][0]["main"] + ".gif"

    def update_time(self, t):
        today = date.today()
        current_time = datetime.datetime.now(LOCAL_TIMEZONE).time()
        self.time.text = current_time.strftime("%H:%M")
        self.date.text = today.strftime(
            "%A, %d" + StringUtils.get_suffix(today) + " of %B")

    def submit(self):
        print("Title ", self.greeting.text)


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{"title": "Retrieving articles...", "description": "Please wait while your news articles are "
                                                                        "retrieved"}]
        self.get_data()

    def get_data(self):
        # get news data from RestAPI
        # UrlRequest(news_api_url, on_success=self.update_view)
        self.data = news_data
        pass

    def update_view(self, request, result):
        # print(result["articles"])
        self.data = StringUtils.format_response(result["articles"][:5])
        # self.data = news_data
        self.refresh_from_data()


class NewsRow(BoxLayout):
    pass


class WindowManager(ScreenManager):
    pass


class MainWindowApp(App):
    def build(self):
        Loader.loading_image = 'images/loading.gif'
        sm = WindowManager()
        sm.add_widget(IdleWindow(name='idle'))
        sm.add_widget(MainWindow(name='main'))

        return sm


if __name__ == "__main__":
    MainWindowApp().run()
