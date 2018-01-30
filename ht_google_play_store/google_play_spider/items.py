# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglePlaySpiderItem(scrapy.Item):
     title = scrapy.Field()
     title_URL = scrapy.Field()
     imgURL = scrapy.Field()
     updatetime=scrapy.Field()
     installtime=scrapy.Field()
     content=scrapy.Field()
     learn_href = scrapy.Field()
     permission=scrapy.Field()

     # description = scrapy.Field()
     # autor = scrapy.Field()
     # autor_URL = scrapy.Field()
     # star_rates = scrapy.Field()
     # price  = scrapy.Field()

