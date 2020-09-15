# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import numpy as np
import logging

from utils.business import LEN_PROPERTIES, MAX_DIF_WITNESS
from main.models import Property, Post, ScrapyJob
from main.utils.constants import RUNNING, FINISHED, FAILED
from scrapy_app.spiders.idealista import ERROR_CODE
from scrapy_app.items import PropertyData
from telegram_bot.errors import report_error

#logging.basicConfig(level=logging.INFO)


class ProcessPostPipeline:

    def __init__(self):

        self.posts = {}

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         unique_id=crawler.settings.get('unique_id'),  # this will be passed from django view
    #     )

    def open_spider(self, spider):
        logging.info('Open spider for job {}'.format(spider.job_id))
        ScrapyJob.objects.filter(pk=spider.job_id).update(status=RUNNING)

    def close_spider(self, spider):
        self._process_posts(spider)

    def process_item(self, item, spider):
        if isinstance(item, PropertyData):
            if item['property_id'] not in self.posts.keys():
                self.posts[item['property_id']] = []
            return item
        values = {key: value[0] for key, value in item.items()}
        try:
            if values['prop_id'] not in self.posts:
                self.posts[values['prop_id']] = []
            if values['link'] not in [post['link'] for post in self.posts[values['prop_id']]]:
                if values['area'] != ERROR_CODE and values['price'] != ERROR_CODE:
                    values['price_sqm'] = values['price']/values['area']
                    prop_id = values.pop('prop_id')
                    self.posts[prop_id].append(values)
                    spider.len_items[prop_id] += 1
            return item
        except Exception as e:
            report_error(spider.user, 'Item Pipeline Error: ' + str(e))
            return item

    def _process_posts(self, spider):
        errors = None
        for prop_id, prop_posts in self.posts.items():
            if len(prop_posts) == 0:
                Property.objects.filter(pk=prop_id).update(done=True)
            try:
                posts_sorted = sorted(prop_posts, key=lambda p: p['price_sqm'])
                top_posts = []
                for i in range(min(LEN_PROPERTIES, len(prop_posts))):
                    if i == 0 or posts_sorted[i]['price_sqm'] < posts_sorted[i-1]['price_sqm'] * (1 + MAX_DIF_WITNESS):
                        top_posts.append(posts_sorted[i])
                    else:
                        break
                avg_price = np.mean([post['price_sqm'] for post in top_posts])
                if not spider.job_id:
                    logging.info('Property {}: {} €/m² from {} posts'.format(prop_id, avg_price, len(posts_sorted)))
                else:
                    post_obj_list = []
                    for i, post in enumerate(top_posts):
                        post_obj_list.append(Post(prop_id=prop_id, index=i+1, link=post['link'], price=post['price'],
                                                  area=post['area'], address=post['name'], distance=post['distance']))
                    Post.objects.bulk_create(post_obj_list)
                    Property.objects.filter(pk=prop_id).update(avg_price=round(avg_price, 2),
                                                               radius=spider.radius[prop_id],
                                                               done=True)
            except Exception as e:
                Property.objects.filter(pk=prop_id).update(valid=False)
                errors = e

        if not errors:
            ScrapyJob.objects.filter(pk=spider.job_id).update(status=FINISHED)
        else:
            ScrapyJob.objects.filter(pk=spider.job_id).update(status=FAILED)
            report_error(spider.user, 'Final Pipeline Error: ' + str(errors))

        logging.info('Done saving data')


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


