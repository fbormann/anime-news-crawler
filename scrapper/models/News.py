from dataclasses import dataclass
from datetime import date
from pony.orm import *
import scrapy

db = Database()


# I know it is a duplicate but it is necessary
class NewsItem(scrapy.Item):
    title = scrapy.Field()
    portal_name = scrapy.Field()
    url = scrapy.Field()
    comment_amount = scrapy.Field()
    word_count = scrapy.Field()
    phrase_count = scrapy.Field()
    paragraph_count = scrapy.Field()
    publish_date = scrapy.Field()


class News(db.Entity):
    title = Required(str)
    portal_name = Required(str)
    url = Required(str, unique=True)
    comment_amount = Required(int)
    word_count = Required(int)
    phrase_count = Required(int)
    paragraph_count = Required(int)
    publish_date = Required(date)
