import scrapy
import logging
from models.News import News
import re
from db_interface.NewsInterface import NewsDBInterface
from datetime import datetime


class AnimeNews(scrapy.Spider):
    name = 'animenews'
    start_urls = ["https://www.animenewsnetwork.com/news"]
    logger = logging.getLogger(__name__)
    news_obj = {}  # use a single instance for better memory management
    news_db_interface = NewsDBInterface()

    def parse(self, response):
        main_feed = response.css('div.mainfeed-section')

        amount_of_news_processed = 0
        for news_item in main_feed.css('div.news.herald'):
            article_link = self.start_urls[0] + news_item.css('div.thumbnail > a::attr(href)').get()
            self.news_obj["url"] = article_link

            if self.news_db_interface.has_item(url=self.news_obj["url"]):
                # there is no need to crawl the same article again
                logging.info("this URL was already crawled: " + self.news_obj["url"])
                return

            comment_element_text = news_item.css('div.comments a::text')
            comment_amount_text_match = re.findall("[\d]*", comment_element_text.get())
            self.news_obj["comment_amount"] = int(comment_amount_text_match[0])
            self.news_obj["title"] = str(news_item.css("div.wrap h3:first-of-type > a::text").get())

            self.news_obj["publish_date"] = datetime.strptime(
                news_item.css("time::attr(datetime)").get(), "%Y-%m-%dT%H:%M:%SZ")

            amount_of_news_processed += 1

            self.logger.info(amount_of_news_processed)
            yield response.follow(self.news_obj["url"], callback=self.parse_article)

    def parse_article(self, response):
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

        self.news_obj["word_count"] = word_count
        self.news_obj["paragraph_count"] = paragraph_count
        self.news_obj["phrase_count"] = sentence_count
        self.news_obj["portal_name"] = self.start_urls[0]
        self.news_db_interface.insert_item(self.news_obj)
