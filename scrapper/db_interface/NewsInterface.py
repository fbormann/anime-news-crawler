from models.News import News


class NewsDBInterface:

    def __init__(self):
        pass

    def insert_item(self, news: News):
        # mock insert news item
        print("news item inserted: " + str(news))
