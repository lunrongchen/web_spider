# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class NewsMarqueDdtItem( scrapy.Item ):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    guid = scrapy.Field()
    pubDate = scrapy.Field()
    description = scrapy.Field()
    
class newsItem ( scrapy.Item ):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class SinaRssItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    guid = scrapy.Field()
    pubDate = scrapy.Field()
    description = scrapy.Field()

class contentItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()

