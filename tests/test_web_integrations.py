import unittest
import requests
import json
import tests.data_utils as data_utils
import cv2

'''
Run tests using $ python -m unittest discover -v tests
'''

# BASE URL ENDPOINT
API_BASE_URL = "http://e1df2ae00187.ngrok.io"

# USER ENDPOINTS
BASIC_AUTH_URL = f"{API_BASE_URL}/auth"
GET_USER_URL = f"{API_BASE_URL}/user"
IDENTIFY_EMOTION_URL = f"{API_BASE_URL}/emotion"

# TEST DATA
user_1 = "alvaro@email.com"
user_2 = "arnold@email.com"
user_3 = "george@email.com"
user_4 = "jennifer@email.com"
user_5 = "tiger@email.com"

PASSWORD = "password"


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        body = {"email": user_1, "password": PASSWORD}
        response = requests.post(BASIC_AUTH_URL, json=body)
        result = json.loads(response.content)
        self.jwt = result["token"]
        self.refresh = result["refreshToken"]
        self.headers = {"Authorization": f"Bearer {self.jwt}"}
        self.refresh_headers = {"Authorization": f"Bearer {self.refresh}"}

    def test_basic_authorization(self):
        body = {"email": user_1, "password": PASSWORD}
        response = requests.post(BASIC_AUTH_URL, json=body)
        self.assertTrue(response.ok)
        result = json.loads(response.content)
        self.assertIsNotNone(result["token"])
        self.assertIsNotNone(result["refreshToken"])

    def test_refresh_jwt(self):
        response = requests.get(BASIC_AUTH_URL, headers=self.refresh_headers)
        result = json.loads(response.content)
        self.assertIsNotNone(result["token"])

    def test_reject_invalid_refresh_token(self):
        response = requests.get(BASIC_AUTH_URL, headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_get_user_data(self):
        response = requests.get(GET_USER_URL, headers=self.headers)
        result = json.loads(response.content)
        self.assertIsNotNone(result["user"])
        self.assertEqual(result["user"]["email"], user_1)


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


if __name__ == '__main__':
    unittest.main()
