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
from imutils.video import VideoStream
import imutils
import time
from requests_toolbelt import MultipartEncoder
import cv2

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

FACE_IDENTIFICATION_URL = "http://3a33572e5cee.ngrok.io/face-recognition"

LOCAL_TIMEZONE = datetime.datetime.now(
    datetime.timezone.utc).astimezone().tzinfo


class IdleWindow(Screen):
    def __init__(self, stream, **kwargs):
        super(IdleWindow, self).__init__(**kwargs)
        self.stream = stream
        self.pending_response = False

        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

        # Clock.schedule_interval(self.change_screen, 5)
        # Clock.schedule_interval(self.detect_face, 1)

    def on_pre_enter(self, **kwargs):
        Clock.schedule_interval(self.detect_face, 1)

    def change_screen(self, user):
        self.manager.transition.direction = 'up'
        self.manager.get_screen('main').set_stuff(user)
        self.manager.current = "main"

    def detect_face(self, t):
        frame = self.stream.read()
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.detector.detectMultiScale(
            gray, minSize=(20, 20), scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            print("face detected")
            # region of interest
            roi_gray = gray[y:y + h, x:x + w]
            cv2.imwrite("image.png", roi_gray)
            if not self.pending_response:
                self.identify_face(roi_gray)
            # Clock.unschedule(self.detect_face)
            # print("Uncheduled")

    def identify_face(self, frame):
        self.pending_response = True
        imencoded = cv2.imencode(".jpg", frame)[1]
        payload = MultipartEncoder(
            fields={
                'files[]': (
                    'image.jpg',
                    imencoded.tostring(),
                    "image/jpeg"
                )
            }
        )
        headers = {
            'Content-Type': payload.content_type
        }
        UrlRequest(
            FACE_IDENTIFICATION_URL,
            req_headers=headers,
            on_success=self.handle_success,
            on_failure=self.handle_fail,
            on_error=self.handle_error,
            req_body=payload
        )

    def handle_success(self, request, result):
        print("success ", result)
        self.change_screen(result["user"])
        Clock.unschedule(self.detect_face)
        self.pending_response = False

    def handle_fail(self, request, result):
        print("fail ", result)
        self.pending_response = False

    def handle_error(self, request, result):
        print("error ", result)
        self.pending_response = False


class MainWindow(Screen):
    greeting = ObjectProperty(None)
    date = ObjectProperty(None)
    time = ObjectProperty(None)
    weather_type = ObjectProperty(None)
    temperature = ObjectProperty(None)
    weather_icon = ObjectProperty(None)

    def __init__(self, stream, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.stream = stream
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
        self.idle = False
        Clock.schedule_interval(self.update_time, 1)

    def on_pre_enter(self, **kwargs):
        Clock.schedule_interval(self.change_screen, 10)
        Clock.schedule_interval(self.go_idle, 1)

    def set_stuff(self, user):
        self.greeting.text = "Hello "+user["firstName"]+"!"
        self.get_weather()

    def change_screen(self, t):
        if self.idle is True:
            self.manager.transition.direction = 'down'
            self.manager.current = "idle"
            self.idle = False
            Clock.unschedule(self.change_screen)
            Clock.unschedule(self.go_idle)

    def go_idle(self, t):
        frame = self.stream.read()
        frame = imutils.resize(frame, width=228)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.detector.detectMultiScale(
            gray, minSize=(20, 20), scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            print("face detected")
            # region of interest
            roi_gray = gray[y:y + h, x:x + w]
            cv2.imwrite("image.png", roi_gray)
            self.idle = False

        if len(faces) == 0:
            self.idle = True

    def get_weather(self):
        # UrlRequest(weather_api_url, on_success=self.update_view,
        #            on_error=self.update_view)
        self.update_view(None, weather)

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
        self.stream = VideoStream(src=0).start()
        time.sleep(2.0)
        sm.add_widget(IdleWindow(self.stream, name='idle'))
        sm.add_widget(MainWindow(self.stream, name='main'))
        return sm


if __name__ == "__main__":
    MainWindowApp().run()
