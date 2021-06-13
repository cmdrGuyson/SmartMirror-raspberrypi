import unittest
import requests
import json
import tests.data_utils as data_utils
import cv2
import tests.config as config
from tests.config import user_1, user_2, user_3, user_4, user_5, PASSWORD

'''
Run tests using $ python -m unittest tests.test_face_recognition_endpoints -v
'''


# BASE URL ENDPOINT
API_BASE_URL = config.API_BASE_URL

# USER ENDPOINTS
BASIC_AUTH_URL = f"{API_BASE_URL}/auth"
FACE_RECOGNITION_URL = f"{API_BASE_URL}/face-recognition"


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


if __name__ == '__main__':
    unittest.main()
