# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
# https://scrapy.readthedocs.org/en/latest/topics/djangoitem.html

#from django.core.urlresolvers import reverse
#from djangotoolbox.fields import ListField, EmbeddedModelField
from scrapy.item import Item, Field
from django.db import models
from scrapy.contrib.djangoitem import DjangoItem


class Plan(models.Model):
    monthlyCost = models.CharField()
    minutes = models.CharField()
    messages = models.CharField()
    data = models.CharField()
    extras = models.CharField()


class PlanItem(DjangoItem):
    django_model = Plan



