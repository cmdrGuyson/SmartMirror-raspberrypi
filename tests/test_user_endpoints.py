import unittest
import requests
import json
import tests.data_utils as data_utils
import tests.config as config
from tests.config import user_1, PASSWORD

'''
Run tests using $ python -m unittest tests.test_user_endpoints -v
'''

# BASE URL ENDPOINT
API_BASE_URL = config.API_BASE_URL

# USER ENDPOINTS
BASIC_AUTH_URL = f"{API_BASE_URL}/auth"
GET_USER_URL = f"{API_BASE_URL}/user"


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
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result["token"])
        self.assertIsNotNone(result["refreshToken"])

    def test_refresh_jwt(self):
        response = requests.get(BASIC_AUTH_URL, headers=self.refresh_headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result["token"])

    def test_reject_invalid_refresh_token(self):
        response = requests.get(BASIC_AUTH_URL, headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_get_user_data(self):
        response = requests.get(GET_USER_URL, headers=self.headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result["user"])
        self.assertEqual(result["user"]["email"], user_1)


if __name__ == '__main__':
    unittest.main()
    output.print_table()
