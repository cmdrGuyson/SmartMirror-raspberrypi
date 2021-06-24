from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import imutils
from requests_toolbelt import MultipartEncoder
import cv2
import os
import time

from env import API_BASE_URL


class IdleWindow(Screen):
    loading = ObjectProperty(None)
    response_label = ObjectProperty(None)

    def __init__(self, stream, **kwargs):
        super(IdleWindow, self).__init__(**kwargs)
        self.stream = stream
        self.pending_response = False

        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

        self.FACE_IDENTIFICATION_URL = f"{API_BASE_URL}/face-recognition"

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

        extracted_faces = []

        for (x, y, w, h) in faces:
            # region of interest
            roi_gray = gray[y:y + h, x:x + w]
            cv2.imwrite("image.png", roi_gray)
            # Add face to list of faces
            extracted_faces.append(roi_gray)

        # If not pending an identification response from the RESTAPI and faces are detected
        # send image to RESTAPI for identification
        if not self.pending_response and len(extracted_faces) > 0:
            self.identify_face(extracted_faces)

    # Identify given face through RESTful API
    def identify_face(self, faces):
        self.pending_response = True

        # Enable loading gif and label
        self.loading.opacity = 1
        self.response_label.text = "Identifying who you are!"

        # Encode images to be sent
        imencoded = []
        for face in faces:
            imencoded.append(cv2.imencode(".jpg", face)[1])

        # Get list of fields
        fields = []
        for encoded in imencoded:
            fields.append(
                ('files[]', ('image.jpg', encoded.tostring(), "image/jpeg")))

        # Create multipart form data for request
        payload = MultipartEncoder(fields=fields)
        headers = {
            'Content-Type': payload.content_type
        }
        UrlRequest(
            self.FACE_IDENTIFICATION_URL,
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
