# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import scrapy
from scrapy.contrib.loader import ItemLoader, Identity
from my_scrapy.items import ImgDownloadItem


class ZhangzishiSpider(scrapy.Spider):
    name = "zhangzishi"
    # allowed_domains = ["zhangzishi.cc"]
    start_urls = [
        'http://www.zhangzishi.cc/index.php?s=%E4%B8%AD%E5%9B%BD%E5%A5%BD%E8%83%B8',
        'http://www.zhangzishi.cc/index.php?s=%E4%B8%AD%E5%9B%BD%E7%BE%8E%E8%85%BF',
        'http://www.zhangzishi.cc/index.php?s=%E4%B8%AD%E5%9B%BD%E5%A5%BD%E8%87%80',
        'http://www.zhangzishi.cc/index.php?s=%E6%B8%85%E6%96%B0%E5%A6%B9%E5%AD%90',
    ]

    def parse(self, response):
        self.logger.info("parse url %s" % response.url)

        sel = Selector(response)
        for link in sel.xpath('//article[@class="excerpt"]/a[@class="thumbnail"]/@href').extract():
            request = scrapy.Request(link, callback=self.parse_item)
            yield request

        sites = sel.xpath("//div[@class='ias_trigger']/a")
        for site in sites:
            next_url = site.xpath('@href').extract()[0]
            name = site.xpath('text()').extract()[0]
            if name == u'下一页':
                request = scrapy.Request(next_url, callback=self.parse)
                yield request

    def parse_item(self, response):
        self.logger.info("parse_item url %s" % response.url)
        l = ItemLoader(item=ImgDownloadItem(), response=response)
        l.add_xpath('name', '//h1[@class="article-title"]/a/text()')
        # l.add_xpath('tags', "//div[@id='maincontent']/div[@class='postmeta  clearfix']/div[@class='metaRight']/p")
        l.add_xpath('image_urls', "//article[@class='article-content']/p/img/@src", Identity())

        l.add_value('url', response.url)
        return l.load_item()
