__author__ = 'root'

import scrapy
from scrapy.contrib.spiders import XMLFeedSpider

from my_scrapy.items import SinaMainItem

class XmlFeedSpiderSample (XMLFeedSpider):
    name = "test2"
    #allowed_domains = ["sina.cn"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"
        #"http://sina.cn/"
    ]

    #'html','xml','iternodes'
    iterator = 'iternodes'
    itertag = 'ul'


    def parse_node(self, response, selector):
        self.log('Hi, this is a <%s> node!: %s' % (self.itertag, ''.join(selector.extract())))

        item = SinaMainItem()
        item['title'] = selector.xpath('a/text()').extract()
        item['url'] = selector.xpath('a/@href').extract()
        item['desc'] = selector.xpath('text()').extract()
        return item



