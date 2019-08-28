from spiders.animenewsspider import AnimeNewsSpider
from scrapy.crawler import CrawlerProcess
import os, sys

if __name__ == '__main__':
    # THIS LINE IS ESSENTIAL TO SOLVE THE PROBLEM OF
    sys.path.append(os.getcwd())
    process = CrawlerProcess()
    process.crawl(AnimeNewsSpider)
    process.start()