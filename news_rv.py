from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout

from utils import StringUtils
import os

# Dummy news data
news_data = [{"title": "Dow Tumbles, But GME Stock Rockets 113%; Bitcoin Surges, As Elon Musk Updates Twitter Bio",
              "description": "The Dow Jones Industrial Average dived 400 points Friday, as the price of Bitcoin "
                             "surged 15% on Tesla CEO Elon Musk's Twitter bio change. GME stock soared."},
             {"title": "SoftBank's Son expects mass production of driverless cars in two years - Reuters",
              "description": "SoftBank Group Corp Chief Executive Masayoshi Son said on Friday he expects mass "
                             "production of self-driving vehicles to start in two years."}]

# NEWS API details
topic = "tesla"
news_api_key = os.environ["NEWS_API_KEY"]
news_api_url = f"https://newsapi.org/v2/top-headlines?language=en&category=entertainment&apiKey={news_api_key}"


class News_RV(RecycleView):
    def __init__(self, **kwargs):
        super(News_RV, self).__init__(**kwargs)
        self.data = [{"title": "Retrieving articles...", "description": "Please wait while your news articles are "
                                                                        "retrieved"}]
        self.get_data()

    def get_data(self):
        # get news data from RestAPI
        # UrlRequest(news_api_url, on_success=self.update_view)
        self.data = news_data
        pass

    def update_view(self, request, result):
        # print(result["articles"])
        self.data = StringUtils.format_response(result["articles"][:5])
        # self.data = news_data
        self.refresh_from_data()


class NewsRow(BoxLayout):
    pass
