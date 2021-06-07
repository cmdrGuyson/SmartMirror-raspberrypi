import unittest
import requests
import json
import tests.data_utils as data_utils
import cv2
import tests.config as config
from tests.config import user_1, user_2, user_3, user_4, user_5, PASSWORD

'''
Run tests using $ python -m unittest discover -v tests
'''

# BASE URL ENDPOINT
API_BASE_URL = config.API_BASE_URL

# USER ENDPOINTS
BASIC_AUTH_URL = f"{API_BASE_URL}/auth"
FACE_RECOGNITION_URL = f"{API_BASE_URL}/face-recognition"
FACE_RECOGNITION_SETUP_URL = f"{API_BASE_URL}/face-setup"


class TestFaceRecognitionEndpoints(unittest.TestCase):

    def test_face_recognition_user1(self):
        for path in data_utils.get_face_recognition_data("alvaro"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                FACE_RECOGNITION_URL, files=file)
            result = json.loads(response.content)
            user = result["user"]
            self.assertEqual(user["email"], user_1)

    def test_face_recognition_user2(self):
        for path in data_utils.get_face_recognition_data("arnold"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                FACE_RECOGNITION_URL, files=file)
            result = json.loads(response.content)
            user = result["user"]
            self.assertEqual(user["email"], user_2)

    def test_face_recognition_user3(self):
        for path in data_utils.get_face_recognition_data("george"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                FACE_RECOGNITION_URL, files=file)
            result = json.loads(response.content)
            user = result["user"]
            self.assertEqual(user["email"], user_3)

    def test_face_recognition_user4(self):
        for path in data_utils.get_face_recognition_data("jennifer"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                FACE_RECOGNITION_URL, files=file)
            result = json.loads(response.content)
            user = result["user"]
            self.assertEqual(user["email"], user_4)

    def test_face_recognition_user5(self):
        for path in data_utils.get_face_recognition_data("tiger"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                FACE_RECOGNITION_URL, files=file)
            result = json.loads(response.content)
            user = result["user"]
            self.assertEqual(user["email"], user_5)

    def test_face_recognition_unknown(self):
        for path in data_utils.get_face_recognition_data("unknown"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                FACE_RECOGNITION_URL, files=file)
            self.assertEqual(response.status_code, 404)


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
