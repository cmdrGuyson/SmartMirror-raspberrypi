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
GET_TWEETS_URL = f"{API_BASE_URL}/tweets"


class TestGetPersonalizedNewsEndpoints(unittest.TestCase):

    def test_get_happy_tweets(self):
        # Login
        body = {"email": user_2, "password": PASSWORD}
        _response = requests.post(BASIC_AUTH_URL, json=body)
        _result = json.loads(_response.content)
        headers = {"Authorization": f"Bearer {_result['token']}"}

        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/happy", headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result["tweets"])

        # Check if tweets are from configured source
        isSuccessful = True

        for tweet in result["tweets"]:
            if tweet["origin"] != "@Motivator":
                isSuccessful = False
                break

        self.assertTrue(isSuccessful)

    def test_get_happy_tweets_without_configuring(self):
        # Login
        body = {"email": user_3, "password": PASSWORD}
        _response = requests.post(BASIC_AUTH_URL, json=body)
        _result = json.loads(_response.content)
        headers = {"Authorization": f"Bearer {_result['token']}"}

        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/happy", headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["error"], "No subscriptions")

    def test_unauthorized_get_happy_tweets(self):
        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/happy")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 401)

    def test_get_sad_tweets(self):
        # Login
        body = {"email": user_2, "password": PASSWORD}
        _response = requests.post(BASIC_AUTH_URL, json=body)
        _result = json.loads(_response.content)
        headers = {"Authorization": f"Bearer {_result['token']}"}

        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/sad", headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result["tweets"])

        # Check if tweets are from configured source
        isSuccessful = True

        for tweet in result["tweets"]:
            if tweet["origin"] != "@DadSaysJokes":
                isSuccessful = False
                break

        self.assertTrue(isSuccessful)

    def test_get_sad_tweets_without_configuring(self):
        # Login
        body = {"email": user_3, "password": PASSWORD}
        _response = requests.post(BASIC_AUTH_URL, json=body)
        _result = json.loads(_response.content)
        headers = {"Authorization": f"Bearer {_result['token']}"}

        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/sad", headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["error"], "No subscriptions")

    def test_unauthorized_get_sad_tweets(self):
        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/sad")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 401)

    def test_get_neutral_tweets(self):
        # Login
        body = {"email": user_2, "password": PASSWORD}
        _response = requests.post(BASIC_AUTH_URL, json=body)
        _result = json.loads(_response.content)
        headers = {"Authorization": f"Bearer {_result['token']}"}

        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/neutral", headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result["tweets"])

        # Check if tweets are from configured source
        isSuccessful = True

        for tweet in result["tweets"]:
            if tweet["origin"] != "@NatGeo":
                isSuccessful = False
                break

        self.assertTrue(isSuccessful)

    def test_get_neutral_tweets_without_configuring(self):
        # Login
        body = {"email": user_3, "password": PASSWORD}
        _response = requests.post(BASIC_AUTH_URL, json=body)
        _result = json.loads(_response.content)
        headers = {"Authorization": f"Bearer {_result['token']}"}

        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/neutral", headers=headers)
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["error"], "No subscriptions")

    def test_unauthorized_get_neutral_tweets(self):
        # Get news
        response = requests.get(f"{GET_TWEETS_URL}/neutral")
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
