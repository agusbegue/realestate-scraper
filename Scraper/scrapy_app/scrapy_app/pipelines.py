# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
from main.models import Post


class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def close_spider(self, spider):
        # And here we are saving our crawled data with django models.
        pass

    def process_item(self, item, spider):
        try:
            post = Post(id=item['id'][0], name=item['name'][0], price=item['price'][0])
            post.save()
        except Exception as e:
            print(str(e))


# class SavePostsPipeline(object):
#     def __init__(self):
#         """
#         Initializes database connection and sessionmaker
#         Creates tables
#         """
#         engine = db_connect()
#         create_table(engine)
#         self.Session = sessionmaker(bind=engine)
#
#     def process_item(self, item, spider):
#         """Save quotes in the database
#         This method is called for every item pipeline component
#         """
#         session = self.Session()
#         post = Post()
#         post.post_name = item['name']
#         post.price = item['price']
#
#         try:
#             session.add(post)
#             session.commit()
#         except:
#             session.rollback()
#             raise
#         finally:
#             session.close()
#
#         return item


