# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiScrapyItems(scrapy.Item):
    # define the fields for your item here like:

    #title = scrapy.Field()
    link = scrapy.Field()
    body = scrapy.Field()

class WikiPageItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()