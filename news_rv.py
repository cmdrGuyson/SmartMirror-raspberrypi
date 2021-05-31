from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock

from utils import StringUtils
import os
import json
import time

with open('dummy_news.json') as f:
    data = json.load(f)

news_data = data["articles"]

# NEWS API details
topic = "tesla"
news_api_key = os.environ["NEWS_API_KEY"]
news_api_url = f"https://newsapi.org/v2/top-headlines?language=en&category=entertainment&apiKey={news_api_key}"


class News_RV(RecycleView):
    def __init__(self, **kwargs):
        super(News_RV, self).__init__(**kwargs)
        self.data = [{"title": "Retrieving articles...", "description": "Please wait while your news articles are "
                                                                        "retrieved"}]
        self.NEWS_URL = f"{os.environ['API_BASE_URL']}/news"

    def get_data(self, token):
        # get news data from RestAPI
        header = {'Authorization': 'Bearer ' + token}
        UrlRequest(self.NEWS_URL, req_headers=header,
                   on_success=self.update_view, on_failure=self.handle_fail, on_error=self.handle_error)
        # self.data = news_data
        pass

    def update_view(self, request, result):
        # Update view after getting data
        if result["articles"] is not None:
            self.data = result["articles"][:6]
            # self.data = news_data
            # self.refresh_from_data()
            Clock.schedule_once(self.handle_refresh, 1)

    def handle_refresh(self, t):
        # Refresh the recycle view
        self.refresh_from_data()
        self.scroll_y = 0

    def handle_fail(self, request, result):

        # Show error messages
        if request._resp_status == 404:
            self.data = [{"title": "You don't seem to have any news subscriptions",
                          "description": "Please subscribe to your favourite news threads from the mobile application"}]
        else:
            self.data = [{"title": "There was an error",
                          "description": "We're very sorry! There was an error while retrieving news articles"}]

        self.refresh_from_data()

    def handle_error(self, request, result):
        self.data = [{"title": "Something went wrong!",
                      "description": "We're very sorry! There was an error while retrieving news articles"}]

        self.refresh_from_data()


class NewsRow(BoxLayout):
    pass
