__author__ = 'root'

import scrapy
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose
from scrapy.utils.response import get_base_url
from scrapy.utils.response import open_in_browser
import urllib
import json
from urlparse import urljoin

from my_scrapy.items import EtodayItem



class EtodaySpider(scrapy.Spider):
    name = "etoday"
    allowed_domains = ["818today.com"]
    start_urls = [
        "http://www.818today.com/xingganmeinv/"
    ]

    def parse(self, response):
        self.log("parse url %s" % response.url)
        base_url = get_base_url(response)
        self.log("base_url %s" % base_url)
        #open_in_browser(response)

        sel = scrapy.Selector(response)
        sites = sel.xpath('//div[@class="pic"]')
        for site in sites:
            url = site.xpath('a/@href').extract()
            sub_url = urljoin(base_url, url[0])
            self.log('sub_url = %s' % sub_url)
            req = scrapy.Request(sub_url, callback=self.parse_sub)
            yield req


    def parse_sub(self, response):
        self.log("parse_sub url %s" % response.url)
        base_url = get_base_url(response)
        #self.log("base_url %s" % base_url)
        #open_in_browser(response)

        item = EtodayItem()

        sel = scrapy.Selector(response)
        sites = sel.xpath('//div[@class="picimg"]')
        for site in sites:
            item['image_urls'] = site.xpath('img/@src').extract()
            item['title'] = site.xpath('img/@title')
            yield item

        sites = sel.xpath('//script[@type="text/javascript"]')
        for site in sites:
	        url = site.xpath('text()').re("NrPicNext=\"(.*?)\"")
	        if len(url) > 0:
		        next_url = urljoin(base_url, url[0])
		        self.log('next_url = %s' % next_url)
		        req = scrapy.Request(next_url, callback=self.parse_sub)
		        yield req
		        break