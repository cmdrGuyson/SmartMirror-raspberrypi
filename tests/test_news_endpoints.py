import unittest
import requests
import json
import tests.data_utils as data_utils
import tests.config as config
from tests.config import user_2, user_3, PASSWORD

'''
Run tests using $ python -m unittest discover -v tests
'''

# BASE URL ENDPOINT
API_BASE_URL = config.API_BASE_URL

# USER ENDPOINTS
BASIC_AUTH_URL = f"{API_BASE_URL}/auth"
GET_NEWS_URL = f"{API_BASE_URL}/news"


class TestGetPersonalizedNewsEndpoints(unittest.TestCase):

    def test_get_personalized_news(self):
        # Login
        body = {"email": user_2, "password": PASSWORD}
        _response = requests.post(BASIC_AUTH_URL, json=body)
        _result = json.loads(_response.content)
        headers = {"Authorization": f"Bearer {_result['token']}"}

        # Get news
        response = requests.get(GET_NEWS_URL, headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result["articles"])

    def test_get_personalized_news_without_configuring(self):
        # Login
        body = {"email": user_3, "password": PASSWORD}
        _response = requests.post(BASIC_AUTH_URL, json=body)
        _result = json.loads(_response.content)
        headers = {"Authorization": f"Bearer {_result['token']}"}

        # Get news
        response = requests.get(GET_NEWS_URL, headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["error"], "No news interests")

    def test_unauthorized_get_personalized_news(self):
        # Get news
        response = requests.get(GET_NEWS_URL)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
