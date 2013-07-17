import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'go.settings'

'''
Runs the scraping. An alternative to running via the crapy command-line
'''

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
#from scrapy import log
from go.spiders.o2 import MySpider
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

def stop_reactor():
    reactor.stop()

dispatcher.connect(stop_reactor, signal=signals.spider_closed)

spider = MySpider()
crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(spider)
crawler.start()
reactor.run()