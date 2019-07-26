# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_name = scrapy.Field()
    item_price = scrapy.Field()
    item_from = scrapy.Field()
    image_list = scrapy.Field()
    aid = scrapy.Field()
    shop_name = scrapy.Field()

    atype = scrapy.Field()
    image_url = scrapy.Field()
    img_paths = scrapy.Field()
