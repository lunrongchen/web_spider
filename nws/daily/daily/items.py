# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

import scrapy

class DailyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class RssItem(scrapy.Item):
	url = scrapy.Field()
	title = scrapy.Field()
	link = scrapy.Field()
	pubDate = scrapy.Field()

class ContentItem(scrapy.Item):
	pass