# -*- coding: utf-8 -*-
import json

from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.http import Request

from scrapy_app.items import PostItem
from main.models import Property
from utils import request_params, map_functions
from utils.business_rules import radius, MIN_WITNESSES
from telegram_bot.errors import report_error


ERROR_CODE = '-1'


class IdealistaSpider(CrawlSpider):

    name = 'idealista'
    base_url = 'https://idealista.com'
    link_url = 'https://www.idealista.com/ajax/listingcontroller/livesearchmapnopins.ajax'
    # allowed_domains = [base_url]

    def __init__(self, *args, **kwargs):

        self.propertys = {}

        self.job_id = kwargs.get('job_id', None)
        if self.job_id:
            for prop in Property.objects.filter(job_id=self.job_id).select_related('job__user'):
                self.propertys[prop.id] = {'latitude': prop.latitude, 'longitude': prop.longitude, 'area': prop.area}
            self.user = prop.job.user.username
        else:
            self.propertys[-1] = {'latitude': 41.41306, 'longitude': 1.93301, 'area': 70}
            self.propertys[-2] = {'latitude': 41.38485, 'longitude': 1.61412, 'area': 120}
            self.propertys[-3] = {'latitude': 41.35175, 'longitude': 1.70743, 'area': 140}
            self.user = 'scrapy_test'

        self.len_items = {prop_id: 0 for prop_id in self.propertys.keys()}
        self.radius = {prop_id: 0 for prop_id in self.propertys.keys()}

        super(IdealistaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        print('Starting requests')
        for prop_id in self.propertys.keys():
            yield self.get_request(prop_id, 1)

    def manage(self, response, prop_id):
        if self.len_items[response.meta.get('prop_id')] < MIN_WITNESSES:
            if response.meta['sweep'] < max(radius.keys()):
                return self.get_request(prop_id, response.meta['sweep'] + 1)
        self.finish_property(response)

    def get_request(self, prop_id, sweep):
        limits = map_functions.get_map_limits(latitude=self.propertys[prop_id]['latitude'],
                                              longitude=self.propertys[prop_id]['longitude'],
                                              radius=radius[sweep])
        extra_params = request_params.get_extra_params(self.propertys[prop_id])
        url = request_params.parse_url(self.link_url, request_params.params + limits + extra_params)
        return Request(url=url, headers=request_params.headers, callback=self.extract_link, errback=self.handle_errors,
                       meta={'prop_id': prop_id, 'sweep': sweep})

    def finish_property(self, response):
        self.radius[response.meta.get('prop_id')] = radius[response.meta['sweep']]

    def extract_link(self, response):
        link = json.loads(response.body)['jsonResponse']['listingSearchUrl']
        url = self.base_url + link
        yield Request(url=url, headers=request_params.headers, callback=self.extract, errback=self.handle_errors,
                      meta=response.meta)

    def extract(self, response):
        try:
            posts = response.css('article.item')
            for post in posts:
                loader = ItemLoader(item=PostItem(), selector=post)
                # meta
                loader.add_value('prop_id', response.meta.get('prop_id'))
                # name
                loader.add_value('name', post.css('.item-link::text').get())
                # price
                loader.add_value('price', post.css('.item-price::text').get() or ERROR_CODE)
                # link
                loader.add_value('link', post.css('.item-link').css('a::attr(href)').get())
                # area
                items = post.css('.item-detail').css('::text').getall()
                area = ERROR_CODE
                for i, item in enumerate(items):
                    if 'm²' in item:
                        area = items[i-1]
                loader.add_value('area', area)
                loader.add_value('distance', radius[response.meta['sweep']])

                yield loader.load_item()

            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.extract, meta=response.meta)
            else:
                yield self.manage(response, response.meta['prop_id'])

        except Exception as e:
            report_error(self.user, 'Extraction Error:' + str(e))

    def handle_errors(self, failure):
        error_code = failure.value.response.status
        if error_code == 403:
            report_error(self.user, 'Request Error: Spider blocked, unable to parse page [403]')
        else:
            report_error(self.user, f'Request Error: Other {error_code}')

    # def handle_errors(self, failure):
    #     response = failure.value.response
    #     if response.status == 403:
    #         print('Error 403, access denied')
    #         if response.meta['retries'] < MAX_RETRIES:
    #             response.meta['retries'] += 1
    #             yield Request(response.url, callback=self.extract, errback=self.handle_errors,
    #                           meta=response.meta, dont_filter=True)
    #         else:
    #             print('max retries')
    #     print('status', response.status)
    #     self.http_status = response.status


