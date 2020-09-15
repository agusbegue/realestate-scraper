# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


class PropertyData(Item):
    property_id = Field()


def parse_dots(text):
    return int(text.strip().replace('.', ''))


class PostItem(Item):
    id = Field()
    name = Field()
    price = Field(input_processor=MapCompose(parse_dots))
    link = Field()
    area = Field(input_processor=MapCompose(parse_dots))
    job_task = Field()
    prop_id = Field()
    distance = Field()


    def __str__(self):
        return ''

