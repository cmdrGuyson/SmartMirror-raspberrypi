import unittest
import requests
import json
import tests.data_utils as data_utils
import cv2
import tests.config as config
from tests.config import user_1, user_2, user_3, user_4, user_5, PASSWORD

'''
Run tests using $ python -m unittest tests.test_face_recognition_setup_endpoints -v
'''


# BASE URL ENDPOINT
API_BASE_URL = config.API_BASE_URL

# USER ENDPOINTS
BASIC_AUTH_URL = f"{API_BASE_URL}/auth"
FACE_RECOGNITION_SETUP_URL = f"{API_BASE_URL}/face-setup"


class TestFaceRecognitionSetupEndpoints(unittest.TestCase):
    def test_face_recognition_setup(self):
        # Login
        body = {"email": user_1, "password": PASSWORD}
        response = requests.post(BASIC_AUTH_URL, json=body)
        result = json.loads(response.content)
        headers = {"Authorization": f"Bearer {result['token']}"}

        # Test setup face recognition
        fields = []

        for path in data_utils.get_face_recognition_setup_data("alvaro"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            fields.append(
                ('files[]', ('image.jpg', imencoded.tobytes(), "image/jpeg")))

        response = requests.post(
            FACE_RECOGNITION_SETUP_URL, files=fields, headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"],
                         "Successfully setup face recognition")

    def test_unauthorized_face_recognition_setup(self):
        # Test setup face recognition
        fields = []

        for path in data_utils.get_face_recognition_setup_data("alvaro"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            fields.append(
                ('files[]', ('image.jpg', imencoded.tobytes(), "image/jpeg")))

        response = requests.post(
            FACE_RECOGNITION_SETUP_URL, files=fields)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 401)

    def test_face_recognition_setup_with_less_images(self):
        # Login
        body = {"email": user_1, "password": PASSWORD}
        response = requests.post(BASIC_AUTH_URL, json=body)
        result = json.loads(response.content)
        headers = {"Authorization": f"Bearer {result['token']}"}

        # Test setup face recognition
        fields = []

        i = 0

        for path in data_utils.get_face_recognition_setup_data("alvaro"):
            i += 1
            if i == 4:
                break
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            fields.append(
                ('files[]', ('image.jpg', imencoded.tobytes(), "image/jpeg")))

        response = requests.post(
            FACE_RECOGNITION_SETUP_URL, files=fields, headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["error"],
                         "Please re-capture images and make sure your face is clear")

    def test_face_recognition_setup_with_images_with_no_face(self):
        # Login
        body = {"email": user_1, "password": PASSWORD}
        response = requests.post(BASIC_AUTH_URL, json=body)
        result = json.loads(response.content)
        headers = {"Authorization": f"Bearer {result['token']}"}

        # Test setup face recognition
        fields = []

        for path in data_utils.get_face_recognition_setup_data("no_face"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            fields.append(
                ('files[]', ('image.jpg', imencoded.tobytes(), "image/jpeg")))

        response = requests.post(
            FACE_RECOGNITION_SETUP_URL, files=fields, headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["error"],
                         "Please re-capture images and make sure your face is clear")


if __name__ == '__main__':
    unittest.main()
