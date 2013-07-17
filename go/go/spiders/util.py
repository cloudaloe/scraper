__author__ = 'matan'
from scrapy import log # This module is useful for printing out debug information

def spider_warning(stage):
    self.log('Spider walk warning %s' % stage)

def spider_broken_exit(stage, details):
    self.log('Spider walk appears to be broken at %s. %s.' % (stage, details))
    exit() # to be refined