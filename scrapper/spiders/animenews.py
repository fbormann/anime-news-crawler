import logging
import re
from datetime import datetime

import scrapy

from db_interface.NewsInterface import NewsDBInterface
from models.News import NewsItem


class AnimeNews(scrapy.Spider):
    name = 'animenews'
    start_urls = ["https://www.animenewsnetwork.com/news"]
    logger = logging.getLogger(__name__)
    news_db_interface = NewsDBInterface()

    custom_settings = {
        "ITEM_PIPELINES": {
            'pipelines.PostgresPipeline.PostgresPipeline': 300
        }
    }

    def parse(self, response):
        main_feed = response.css('div.mainfeed-section')

        amount_of_news_processed = 0
        for news_item in main_feed.css('div.news.herald'):
            article_link = self.start_urls[0] + news_item.css('div.thumbnail > a::attr(href)').get()
            news_obj = NewsItem()  # use a single instance for better memory management
            news_obj["url"] = article_link

            if self.news_db_interface.has_item(url=news_obj["url"]):
                # there is no need to crawl the same article again
                logging.info("this URL was already crawled: " + news_obj["url"])
                return

            comment_element_text = news_item.css('div.comments a::text')
            comment_amount_text_match = re.findall("[\d]*", comment_element_text.get())
            news_obj["comment_amount"] = int(comment_amount_text_match[0])
            news_obj["title"] = str(news_item.css("div.wrap h3:first-of-type > a::text").get())

            news_obj["publish_date"] = datetime.strptime(
                news_item.css("time::attr(datetime)").get(), "%Y-%m-%dT%H:%M:%SZ")

            amount_of_news_processed += 1

            self.logger.info(amount_of_news_processed)
            logging.debug(news_obj)
            yield response.follow(news_obj["url"], callback=self.parse_article, cb_kwargs={"news_obj": news_obj})

    def parse_article(self, response, news_obj):
        main_content_div = response.css("div.meat")
        paragraph_count = 0
        word_count = 0
        sentence_count = 0
        for paragraph in main_content_div.css("p"):
            paragraph_children_text = paragraph.css("*::text")

            paragraph_text = []
            for tag_text in paragraph_children_text:
                paragraph_text.append(tag_text.get())
            paragraph_text = " ".join(paragraph_text)
            word_count += len(paragraph_text.split())
            sentence_count += len(paragraph_text.split("."))
            paragraph_count += 1

        news_obj["word_count"] = word_count
        news_obj["paragraph_count"] = paragraph_count
        news_obj["phrase_count"] = sentence_count
        news_obj["portal_name"] = self.start_urls[0]
        logging.debug("news object being yielded")
        logging.debug(news_obj)
        yield news_obj
