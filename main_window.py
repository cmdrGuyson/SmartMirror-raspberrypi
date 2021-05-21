from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.loader import Loader
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from requests_toolbelt import MultipartEncoder

import datetime
from datetime import date
import imutils
import time
import cv2
import os

from utils import StringUtils
from dotenv import load_dotenv

from emotion_recognizer import EmotionRecognizer

load_dotenv()

CITY = "Colombo"
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
UNITS = "metric"
weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units={UNITS}"

weather = {"main": {"temp": 25.5}, "weather": [{
    "main": "Thunder", "description": "broken clouds"}]}

LOCAL_TIMEZONE = datetime.datetime.now(
    datetime.timezone.utc).astimezone().tzinfo


class MainWindow(Screen):
    greeting = ObjectProperty(None)
    date = ObjectProperty(None)
    time = ObjectProperty(None)
    weather_type = ObjectProperty(None)
    temperature = ObjectProperty(None)
    weather_icon = ObjectProperty(None)
    news_rv = ObjectProperty(None)
    emotion = ObjectProperty(None)

    def __init__(self, stream, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.stream = stream
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
        self.idle = False
        self.identifying_emotion = False
        self.EMOTION_IDENTIFICATION_URL = f"{os.environ['API_BASE_URL']}/emotion"
        self.emotionRecognizer = EmotionRecognizer()

    def on_pre_enter(self, **kwargs):
        Clock.schedule_interval(self.change_screen, 60*5)
        Clock.schedule_interval(self.monitor_activity, 1)
        Clock.schedule_interval(self.update_time, 1)
        pass

    def set_stuff(self, user):
        self.greeting.text = "Hello "+user["firstName"]+"!"
        self.get_weather()
        self.user = user
        self.token = user["token"]
        self.get_news()

    def change_screen(self, t):
        if self.idle is True:
            self.manager.transition.direction = 'down'
            self.manager.current = "idle"
            self.idle = False
            Clock.unschedule(self.change_screen)
            Clock.unschedule(self.monitor_activity)

    def get_news(self):
        self.news_rv.get_data(self.token)

    def monitor_activity(self, t):
        frame = self.stream.read()
        frame = imutils.resize(frame, width=228)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.detector.detectMultiScale(
            gray, minSize=(20, 20), scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            # region of interest
            roi_gray = gray[y:y + h, x:x + w]
            self.idle = False
            self.handle_emotion_identification(roi_gray)

        if len(faces) == 0:
            self.idle = True

    def handle_emotion_identification(self, frame):
        self.current_emotion = self.emotionRecognizer.identify_emotion(
            cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
        self.emotion.source = "images/"+self.current_emotion+".png"

    def identify_emotion(self, frame):
        if not self.identifying_emotion:
            self.identifying_emotion = True

            # Encode image to be sent
            imencoded = cv2.imencode(".jpg", frame)[1]

            # Create multipart form data for request
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
                'Content-Type': payload.content_type,
                'Authorization': 'Bearer ' + self.token
            }
            UrlRequest(
                self.EMOTION_IDENTIFICATION_URL,
                req_headers=headers,
                on_success=self.handle_success,
                on_failure=self.handle_fail,
                on_error=self.handle_error,
                req_body=payload
            )

    def handle_success(self, request, result):
        print("[INFO] Success", result["emotion"])
        self.current_emotion = result["emotion"]
        self.identifying_emotion = False
        self.emotion.source = "images/"+self.current_emotion+".png"

    def handle_fail(self, request, result):
        print("[INFO] Fail")
        self.identifying_emotion = False

    def handle_error(self, request, result):
        print("[INFO] error")
        self.identifying_emotion = False

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
