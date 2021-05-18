from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest

from utils import StringUtils
import os
import json

# Dummy news data
news_data = [{"title": "Dow Tumbles, But GME Stock Rockets 113%; Bitcoin Surges, As Elon Musk Updates Twitter Bio",
              "description": "The Dow Jones Industrial Average dived 400 points Friday, as the price of Bitcoin "
                             "surged 15% on Tesla CEO Elon Musk's Twitter bio change. GME stock soared."},
             {"title": "SoftBank's Son expects mass production of driverless cars in two years - Reuters",
              "description": "SoftBank Group Corp Chief Executive Masayoshi Son said on Friday he expects mass "
                             "production of self-driving vehicles to start in two years."}]

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
        UrlRequest(news_api_url, req_headers=header,
                   on_success=self.update_view, on_failure=self.handle_fail, on_error=self.handle_error)
        # self.data = news_data
        pass

    def update_view(self, request, result):
        self.data = StringUtils.format_response(result["articles"])
        # self.data = news_data
        self.refresh_from_data()

    def handle_fail(self, request, result):

        # Hide loading gif and change label
        self.loading.opacity = 0
        if request._resp_status == 404:
            self.data = [{"title": "You don't seem to have any news subscriptions",
                          "description": "Please subscribe to your favourite news threads from the mobile application"}]
        else:
            self.data = [{"title": "There was an error",
                          "description": "We're very sorry! There was an error while retrieving news articles"}]

        self.refresh_from_data()

    def handle_error(self, request, result):
        self.data = [{"title": "Somthing went wrong!",
                      "description": "We're very sorry! There was an error while retrieving news articles"}]
        
        self.refresh_from_data()


class NewsRow(BoxLayout):
    pass
