import os
from models.News import News
from models.News import db
from pony.orm import *


class PostgresPipeline(object):
    table_name = "news"

    def __init__(self, host, db_user, db_password, db_port):
        self.db_host = host
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=os.environ.get("DB_HOST"), db_user=os.environ.get("DB_USER"),
                   db_password=os.environ["DB_PWD"], db_port=os.environ["DB_PORT"])

    def open_spider(self, spider):
        self.db = db
        self.db.bind(provider="postgres", host=self.db_host, user=self.db_user,
                     password=self.db_password)
        self.db.generate_mapping(create_tables=True)

    def close_spider(self, spider):
        self.db.disconnect()

    @db_session
    def process_item(self, item, spider):
        if News.select(lambda n: n.url == item["url"]).count() == 0:
            # insert item
            News(**item)
        return item
