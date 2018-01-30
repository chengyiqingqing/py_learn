# coding=utf8
from google_play_spider.items import GooglePlaySpiderItem
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor

import scrapy

class PttSpider(CrawlSpider):
    name = "playspider"
    allowed_domains = ["play.google.com"]
    start_urls = [
       "https://play.google.com/store/apps/details?id=mobi.infolife.ezweather.widget.batteryandweather",
        "https://play.google.com/store/apps/details?id=mobi.infolife.ezweather.widget.localweatherapp",
       #  "https://play.google.com/store/apps/details?id=mobi.infolife.ezweather"

    ]
    rules = [
        Rule(LinkExtractor(allow=(r"id=mobi.infolife.ezweather.widget.(batteryandweather|localweatherapp)")), callback='parse_app',
             follow=False)
<<<<<<< HEAD
    ]  # CrawlSpider 会根据 rules 规则爬取页面并调用函数进行处理 .widget.(batteryandweather|localweatherapp)
=======
    ]  # CrawlSpider 会根据 rules 规则爬取页面并调用函数进行处理
>>>>>>> f5fece91c45c0cff50366993fc577419a843dbf8

    def parse_app(self, response):
        # 在这里只获取页面的 URL 以及下载数量
        item = GooglePlaySpiderItem()
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

        return item
