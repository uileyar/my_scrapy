__author__ = 'root'

import scrapy
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose
from scrapy.utils.response import get_base_url
from scrapy.utils.response import open_in_browser
import urllib
import json
from urlparse import urljoin

from my_scrapy.items import LawsonItem


class StoreLoader(XPathItemLoader):
    default_output_processor = Compose(lambda v: v[0], unicode.strip)


class LawsonSpider(scrapy.Spider):
    name = "lawson"
    allowed_domains = ["lawson.com.cn"]
    start_urls = [
        "http://www.lawson.com.cn/store"
    ]

    def parse(self, response):
        self.log("parse url %s" % response.url)
        base_url = get_base_url(response)
        self.log("base_url %s" % base_url)
        open_in_browser(response)

        api_url = '/api/v1/stores?'

        d = {'city': 'temp', 'district': '', 'keyword': ''}

        sel = scrapy.Selector(response)
        sites = sel.xpath('//select[@id="store_city"]/option')
        for site in sites:
            option = site.xpath('text()').extract()
            self.log('option = %s' % option)

            d['city'] = option[0].encode('utf8')
            # self.log('city = %s' % d['city'])

            url = urljoin(base_url, api_url + urllib.urlencode(d))
            self.log('url = %s' % url)
            req = scrapy.Request(url, callback=self.parse_geo)
            yield req

    def parse_geo(self, response):
        self.log("parse_geo url %s" % response.url)
        dicts = json.loads(response.body)

        item = LawsonItem()
        for dic in dicts:
            item['city'] = dic['city']
            item['address'] = dic['address']
            item['coords'] = dic['coords']
            item['district'] = dic['district']
            item['name'] = dic['name']
            item['tel'] = dic['tel']
            item['id'] = dic['id']

            yield item

