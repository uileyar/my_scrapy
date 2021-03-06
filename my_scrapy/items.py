# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class DomzMainItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
    last = scrapy.Field()


class SinaMainItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()


class LawsonItem(scrapy.Item):
    city = scrapy.Field()
    address = scrapy.Field()
    coords = scrapy.Field()
    district = scrapy.Field()
    name = scrapy.Field()
    tel = scrapy.Field()
    id = scrapy.Field()


class EtodayItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class MeizituItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class FileDownloadItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

    url = scrapy.Field()
    name = scrapy.Field()
    tags = scrapy.Field()


class ImgDownloadItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join(), )
    desc = scrapy.Field(output_processor=Join(u', '),)
    image_urls = scrapy.Field()
    images = scrapy.Field()
