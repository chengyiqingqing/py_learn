# coding=utf8
from google_play_spider.items import Item
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor

import scrapy

class PttSpider(CrawlSpider):
    name = "sww"
    allowed_domains = ["play.google.com"]
    start_urls = [
     # "https://play.google.com/store/apps/details?id=mobi.infolife.ezweather"
     "https://play.google.com/store/apps/details?id=mobi.infolife.ezweatherlite"

    ]
    rules = [
        Rule(LinkExtractor(allow=("id=mobi.infolife.ezweather")), callback='parse',
             follow=False)
    ]  # 正则表达式匹配  .widget.(batteryandweather|localweatherapp)

    def parse(self, response):

        item = Item()
        # item['title_URL'] = response.url
        # item['title'] = response.xpath("//div[@class='id-app-title']").xpath("text()").extract()
        # item['imgURL'] = response.xpath("//img[@alt = 'Cover art']/@src").extract()
        item['updatetime'] = response.xpath(
            "//div[@class='details-section-contents']/div[@class='meta-info']/div[@class='content']/text()").extract()
        item['title'] = response.xpath(
            "//div[@class='details-section-contents']/div[@class='meta-info contains-text-link']/div[@class='content']/text()").extract()
        item['content']=response.xpath(
            "//div[@class='details-section-contents']/div[@class='meta-info contains-text-link']/a/text()").extract()
        item['learn_href'] = response.xpath(
            "//div[@class='details-section-contents']/div[@class='meta-info contains-text-link']/a/@href").extract()
        item['permission'] = response.xpath(
            "//div[@class='details-section-contents']/div[@class='meta-info contains-text-link']/button/@data - docid").extract()
        return item

        # sites = response.css('div.details-section metadata')
        # items = []
        # for site in sites:
        #
        #     item = GooglePlaySpiderItem()
        #     item['updatetime']=site
        #     item['updatetime'] = site.css(
        #         'div.details-section-contents > div.meta-info > div.content::text').extract().strip()
        #     item['installtime'] = site.xpath(
        #         'div.details-section-contents > div.meta-info > div.content::text').extract().strip()
        #     items.append(item)
        # return items


