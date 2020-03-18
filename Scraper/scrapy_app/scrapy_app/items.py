# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def parse_dots(text):
    return int(text.replace('.', ''))

def link_generator(text):
    return 'idealista.com' + text

class PostItem(Item):
    id = Field()
    name = Field()
    price = Field(input_processor=MapCompose(parse_dots))
    link = Field(input_processor=MapCompose(link_generator))
    meters = Field(input_processor=MapCompose(parse_dots))






