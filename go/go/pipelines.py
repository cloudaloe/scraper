# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy import signals
from scrapy.exceptions import DropItem

class DjangoSaver(object):
    def process_item(self, item, spider):
        item.save()
        #raise DropItem()
        return item

