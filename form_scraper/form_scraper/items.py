# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class Form(Item):
    url = Field()
    given_class = Field()
    given_type = Field()
