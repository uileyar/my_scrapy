__author__ = 'root'

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from my_scrapy.items import DomzMainItem
from my_scrapy.items import Product
from urlparse import urlparse

class DomzSpider (scrapy.Spider):
    name = "domz"
    allowed_domains = ["domz.org"]
    start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def __init__(self, category=None, *args, **kwargs):
        super(DomzSpider, self).__init__(*args, **kwargs)

    def itemTest(self):
        product = Product(name='Desktop PC', price=1000)
        print product.get('last_updated', 'not set')
        print product.get('lala', 'unknown field')
        print 'name in product:','name' in product
        print 'name in product.fields:','name' in product.fields
        print 'stock in product:','stock' in product
        print 'last_updated in product:','last_updated' in product
        print 'last_updated in product.fields:','last_updated' in product.fields
        print 'lala in product:', 'lala' in product

    def parse_item(self, response):
        self.log('parse_item: %s' % response.url)




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



