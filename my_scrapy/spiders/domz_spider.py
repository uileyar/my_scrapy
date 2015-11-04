__author__ = 'root'

import scrapy

from my_scrapy.items import MyScrapyItem

class DomzSpider (scrapy.Spider):
    name = "domz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, "wb") as f:
        #    f.write(response.body)

        for sel in response.xpath('//ul/li'):
            item = MyScrapyItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['url']   = sel.xpath('a/@href').extract()
            item['desc']  = sel.xpath('text()').extract()
            yield item
