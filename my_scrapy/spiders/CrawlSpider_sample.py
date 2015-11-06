__author__ = 'root'

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from my_scrapy.items import DomzMainItem
from my_scrapy.items import Product
from urlparse import urlparse


class CrawlSpiderSample (CrawlSpider):
    name = "test1"
    allowed_domains = ["sina.cn"]
    start_urls = [
       "http://sina.cn/"
    ]

    rules = (
        Rule(LinkExtractor(allow=('daily', ), deny=('subsection\.php', )), callback='parse_item1'),

        #Rule(LinkExtractor(allow=('python', )), callback='parse_item2'),
    )

    def parse_item1(self, response):
        self.log('parse_item1: %s' % response.url)


    def parse_item2(self, response):
        self.log('parse_item2: %s' % response.url)


    def parse_normal(self, response):
        self.log('parse_normal: %s' % response.url)
        #filename = response.url.split("/")[-2]
        #with open(filename, "wb") as f:
        #    f.write(response.body)

        items = []
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        sel = scrapy.Selector(response)
        sites = sel.xpath('//ul[@class="directory-url"]/li')

        for site in sites:
            item = DomzMainItem()
            item['title'] = site.xpath('a/text()').extract()
            item['url'] = url = site.xpath('a/@href').extract()[0]
            item['desc'] = site.xpath('text()').extract()
            yield item
            #items.append(item)

            self.log('url1 %s' % item.get('url'))
            parsed_suburi = urlparse(url)

            if len('{uri.scheme}'.format(uri=parsed_suburi)) > 0:
                url = domain + url

            self.log('url2 %s' % item.get('url'))
            yield scrapy.Request(url, callback=self.parse)


        #return items



