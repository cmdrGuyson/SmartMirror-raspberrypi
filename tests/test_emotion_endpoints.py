import unittest
import requests
import json
import tests.data_utils as data_utils
import cv2
import tests.config as config
from tests.config import user_1, PASSWORD

'''
Run tests using $ python -m unittest tests.test_emotion_endpoints -v
'''

# BASE URL ENDPOINT
API_BASE_URL = config.API_BASE_URL

# USER ENDPOINTS
BASIC_AUTH_URL = f"{API_BASE_URL}/auth"
IDENTIFY_EMOTION_URL = f"{API_BASE_URL}/emotion"


class TestEmotionEndpoints(unittest.TestCase):
    def setUp(self):
        body = {"email": user_1, "password": PASSWORD}
        response = requests.post(BASIC_AUTH_URL, json=body)
        result = json.loads(response.content)
        self.jwt = result["token"]
        self.headers = {"Authorization": f"Bearer {self.jwt}"}

    def test_identify_happy_emotions(self):
        for path in data_utils.get_emotion_data("happy"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                IDENTIFY_EMOTION_URL, files=file, headers=self.headers)
            result = json.loads(response.content)
            self.assertEqual(result["emotion"], "happy")

    def test_identify_sad_emotions(self):
        for path in data_utils.get_emotion_data("sad"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                IDENTIFY_EMOTION_URL, files=file, headers=self.headers)
            result = json.loads(response.content)
            self.assertEqual(result["emotion"], "sad")

    def test_identify_neutral_emotions(self):
        for path in data_utils.get_emotion_data("neutral"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                IDENTIFY_EMOTION_URL, files=file, headers=self.headers)
            result = json.loads(response.content)
            self.assertEqual(result["emotion"], "neutral")

    def test_unauthorized_identify_emotions(self):
        for path in data_utils.get_emotion_data("happy"):
            image = cv2.imread(path)
            imencoded = cv2.imencode(".jpg", image)[1]
            file = {'files[]': (
                'image.jpg', imencoded.tobytes(), 'image/jpeg')}
            response = requests.post(
                IDENTIFY_EMOTION_URL, files=file)
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
