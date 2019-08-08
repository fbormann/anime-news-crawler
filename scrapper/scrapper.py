import scrapy


class AnimeNews(scrapy.Spider):
    name = 'animenews'
    start_urls = ["https://www.animenewsnetwork.com/news/"]

    # allowed_domains = ["animenewsnetwork.com"]

    def parse(self, response):
        main_feed = response.css('div.mainfeed-section')

        for news_item in main_feed.css('div.news.herald'):
            print(news_item.get())
            comment_element = news_item.css('div.comments')
            print(comment_element.get())
            title_element = news_item.css("div.wrap")
            print(title_element.get())
            print("title text: " + str(news_item.css("div.wrap h3:first-of-type > a::text").get()))
            article_link_element = news_item.css('div.thumbnail > a::attr(href)')
            print(article_link_element.get())
