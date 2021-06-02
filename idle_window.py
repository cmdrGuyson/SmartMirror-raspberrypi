from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import imutils
from requests_toolbelt import MultipartEncoder
import cv2
import os
import time

FACE_IDENTIFICATION_URL = f"{os.environ['API_BASE_URL']}/face-recognition"


class IdleWindow(Screen):
    loading = ObjectProperty(None)
    response_label = ObjectProperty(None)

    def __init__(self, stream, **kwargs):
        super(IdleWindow, self).__init__(**kwargs)
        self.stream = stream
        self.pending_response = False

        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

    # Change display properties and schedule events on enter
    def on_pre_enter(self, **kwargs):
        # Hide loading gif and change label
        self.loading.opacity = 0
        self.response_label.text = " "
        Clock.schedule_interval(self.detect_face, 2)
        pass

    # Change screen to main after successfully recognizing face
    def change_screen(self, data):
        self.manager.transition.direction = 'up'
        self.manager.get_screen('main').configure_screen(data["user"])
        self.manager.current = "main"

    # Detect if a face is present
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

    # Identify given face through RESTful API
    def identify_face(self, frame):
        self.pending_response = True

        # Enable loading gif and label
        self.loading.opacity = 1
        self.response_label.text = "Identifying who you are!"

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

    # Log user in after successfully identifying face
    def handle_success(self, request, result):
        # Hide loading gif and change label
        self.response_label.text = "Welcome back! Logging you in..."

        print("success ", result)
        self.change_screen(result)
        Clock.unschedule(self.detect_face)
        self.pending_response = False

    # Unsuccessful attempt at identifying face
    def handle_fail(self, request, result):

        # Hide loading gif and change label
        self.loading.opacity = 0
        if request._resp_status == 404:
            self.response_label.text = "I don't think I know you!"
        else:
            self.response_label.text = "Something went wrong!"

        self.pending_response = False

    # Error on identifying face
    def handle_error(self, request, result):
        # Hide loading gif and change label
        self.loading.opacity = 0
        self.response_label.text = "Something went wrong!"

        print("error ", result)
        self.pending_response = False
