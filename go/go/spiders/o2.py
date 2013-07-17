#TODO: wrap XPath selects that should result in only one node with verification (& confirm no performance impact)
#TODO: consider verbose mode that outputs results of parsing steps even when parsing is as expected
#TODO: use proper logger
#TODO: turn url's and crawl steps into configuration
#TODO: use proper exception catching strategy
#TODO: unit test for every function
#TODO: system test against offline html copies

'''
Add django environment variable required by django code,
as this scrapy code depends on django (otherwise scrapy command-line fails).
'''
#TODO: Should be bash script instead
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'go.settings'
from go.models import PlanItem

__author__ = 'matan'
from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest, Request
from scrapy.item import Item, Field
from sys import exit
import util


class MySpider(BaseSpider):
    name = 'www.o2.co.uk'
    allowed_domains = ['www.o2.co.uk']
    start_urls = [
        'https://www.o2.co.uk/shop/tariffs/?commitmentLengthValues=24%20Months'
        #'https://www.o2.co.uk/shop/tariffs/?commitmentLengthValues=18%20Months'
    ]

    def get_phone_picture(self, response):
        self.log('Getting phone picture....')

    def get_phone_picture_err(self, failure,):
        # TODO: beef up
        self.log('at errbck')

    def parse_phones(self, response):

        '''
        phone details handler
        '''

        self.log('Parsing phones....')

        hxs = HtmlXPathSelector(response)
        phones = hxs.select('//ul[@id="handsetList"]/li')
        print 'number of phones:  %d' % len(phones)

        if not phones:
            util.spider_broken_exit(stage='locating phones on phones page', details='no phones located' )
        else:
            for phone in phones:
                #TODO: raise error if following details not found
                #TODO: implement errback
                brand = phone.select('.//span[contains(@class, "brand")]/text()').extract()
                model = phone.select('.//span[contains(@class, "model")]/text()').extract()
                picture_url = phone.select('.//a/img/@src').extract()

                print brand + model + picture_url
                print 'picture-url is %s' % 'https://www.o2.co.uk'+picture_url[0]

                yield Request(url = 'https://www.o2.co.uk'+picture_url[0], callback = self.get_phone_picture, errback = self.get_phone_picture_err )

    def follow_form_link(self, form):
        print('following form link....')
        form_field_names = form.select('input/@name') .extract()
        form_field_values = form.select('input/@value') .extract()
        form_fields = dict(zip(form_field_names, form_field_values))
        #form_fields = {'tariffId' : 'a7f2c7b8-cfad-403e-9ec1-05fd997ee0d5', 'dataAllowanceName' : '100MB'}

        print form_fields
        return FormRequest(url="https://www.o2.co.uk/shop/phones/", method='GET', formdata=form_fields, callback=self.parse_phones)

    def parse(self, response):

        '''
        Plans page handler.
        This function is call-backed from the spider's initial crawl
        '''

        self.log('Obtained response from %s' % response.url)
        self.log('Parsing plans....')
        hxs = HtmlXPathSelector(response)
        plans = hxs.select('//tr[td[contains(@class, "monthlyCost")]]')

        if not plans:
            util.spider_broken_exit(stage='locating plans on plans page', details='no plans located' )
        else:
            for plan in plans:
                #print plan.extract()

                item = PlanItem()

                item['monthlyCost'] = plan.select('td[contains(@class, "monthlyCost")]/text()').extract()
                item['minutes'] = plan.select('td/span[contains(@class, "minsVal")]/text()').extract()
                item['messages'] = plan.select('td/span[contains(@class, "textsVal")]/text()').extract()
                item['data'] = plan.select('td/span[contains(@class, "dataAllowance")]/text()').extract()
                item['extras'] = plan.select('td/span[contains(@class, "extras")]/span/text()').extract()

                phone_link = plan.select('.//form')

                print plan
                print(phone_link).extract()

                yield self.follow_form_link(form = phone_link)
                yield item

                #link = site.select('a/@href').extract()
                #desc = site.select('text()').extract()
                #print title, link, desc

