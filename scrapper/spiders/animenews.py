import scrapy
import logging


class AnimeNews(scrapy.Spider):
    name = 'animenews'
    start_urls = ["https://www.animenewsnetwork.com/news/"]
    logger = logging.getLogger(__name__)

    # allowed_domains = ["animenewsnetwork.com"]

    def parse(self, response):
        main_feed = response.css('div.mainfeed-section')

        amount_of_news_processed = 0
        for news_item in main_feed.css('div.news.herald'):
            self.logger.debug(news_item.get())
            comment_element = news_item.css('div.comments')
            self.logger.debug(comment_element.get())
            title_element = news_item.css("div.wrap")
            self.logger.debug(title_element.get())
            self.logger.debug("title text: " + str(news_item.css("div.wrap h3:first-of-type > a::text").get()))
            article_link_element = news_item.css('div.thumbnail > a::attr(href)')
            self.logger.debug(article_link_element.get())
            amount_of_news_processed += 1
            self.logger.debug(amount_of_news_processed)