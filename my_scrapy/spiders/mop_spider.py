# -*- coding: utf-8 -*-
from urlparse import urljoin
from scrapy.selector import Selector
import scrapy
from scrapy.contrib.loader import ItemLoader, Identity
from my_scrapy.items import ImgDownloadItem
from scrapy.utils.response import get_base_url


class MopSpider(scrapy.Spider):
	name = "mop"
	# allowed_domains = ["tt.mop.com"]
	start_urls = ['http://tt.mop.com/c35.html', ]

	def parse(self, response):
		self.logger.info("parse url %s" % response.url)
		base_url = get_base_url(response)
		has_item = False

		sel = Selector(response)

		sites = sel.xpath('//div[@class="tt-postBox fl mr25 mb20"]/div/div[@class="postTitle"]/a')
		for site in sites:
			has_item = True
			url = site.xpath('@href').extract()
			next_url = urljoin(base_url, url[0])
			#self.logger.info("item url %s" % next_url)
			request = scrapy.Request(next_url, callback=self.parse_item)
			yield request

		if has_item == False:
			return

		sites = sel.xpath("//div[@class='m-page']/a")
		for site in sites:
			next_url = site.xpath('@href').extract()[0].strip()
			name = site.xpath('text()').extract()[0]
			if name == u'下一页':
				request = scrapy.Request(next_url, callback=self.parse)
				yield request

	def parse_item(self, response):
		self.logger.info("parse_item url %s" % response.url)
		l = ItemLoader(item=ImgDownloadItem(), response=response)

		l.add_xpath('name', '//h1[@class="c333 subTitle"]/text()')
		l.add_xpath('image_urls', "//p[@class='tc mb10']/img/@src", Identity())

		l.add_value('url', response.url)
		return l.load_item()
