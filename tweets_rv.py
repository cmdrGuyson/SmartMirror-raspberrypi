from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ListProperty
from kivy.clock import Clock

from utils import StringUtils
import os
import json
import time

from env import API_BASE_URL


class Tweets_RV(RecycleView):
    def __init__(self, **kwargs):
        super(Tweets_RV, self).__init__(**kwargs)
        self.data = [{"origin": "I'm figuring out your emotion...",
                      "tweet": "Please wait while your emotion is calculated. This may take a little time"}]
        self.TWEETS_URL = f"{API_BASE_URL}/tweets"

    def get_data(self, token, emotion):
        # get tweets for current emotion from RestAPI
        header = {'Authorization': 'Bearer ' + token}
        UrlRequest(f"{self.TWEETS_URL}/{emotion}", req_headers=header,
                   on_success=self.update_view, on_failure=self.handle_fail, on_error=self.handle_error)
        pass

    def update_view(self, request, result):
        # Update view on results
        if result["tweets"] is not None:

            # tweets = [{"origin": tweet["origin"], "tweet": tweet["tweet"]} for tweet in result["tweets"]]
            # self.data = ListProperty(tweets)

            self.data = result["tweets"][:6]
            # self.data = news_data
            # self.refresh_from_data()
            Clock.schedule_once(self.handle_refresh, 1)

    def handle_refresh(self, t):
        self.refresh_from_data()
        self.scroll_y = 0

    def handle_fail(self, request, result):

        # Show error message
        if request._resp_status == 404:
            self.data = [{"origin": "You don't seem to have any twitter subscriptions for current emotion",
                          "tweet": "Please subscribe to your favourite twitter feeds from the mobile application"}]
        else:
            self.data = [{"origin": "There was an error",
                          "tweet": "We're very sorry! There was an error while retrieving tweets"}]

        self.refresh_from_data()

    def handle_error(self, request, result):
        self.data = [{"origin": "Something went wrong!",
                      "tweet": "We're very sorry! There was an error while retrieving tweets"}]

        self.refresh_from_data()


class TweetRow(BoxLayout):
    pass
