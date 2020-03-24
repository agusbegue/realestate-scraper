# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import Request, Response
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from scrapy_app.items import PostItem
from scrapy_app.settings import MAX_RETRIES


class IdealistaSpider(CrawlSpider):
    name = 'idealista'
    #base_url = 'https://idealista.com'
    start_urls = ['https://www.idealista.com/venta-viviendas/barcelona-barcelona/']

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        # self.start_urls = [self.url]
        # self.allowed_domains = [self.domain]

        IdealistaSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(IdealistaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        print('entro start_reqs', self.start_urls)
        yield Request(url=self.start_urls[0], callback=self.parsear, errback=self.handle_errors, meta={'retries': 0})

    def parsear(self, response):
        print('entro a {}'.format(response.url))
        print(response.meta.get("proxy"))
        response.meta['retries'] = 0
        try:
            posts = response.css('article.item')
            for post in posts:
                loader = ItemLoader(item=PostItem(), selector=post)
                # loader.add_value('id', i)
                # name
                loader.add_value('name', post.css('.item-link::text').get())
                # price
                loader.add_value('price', post.css('.item-price::text').get())
                # link
                loader.add_value('link', post.css('.item-link').css('a::attr(href)').get())
                # meters
                items = post.css('.item-detail').css('::text').getall()
                meters = '-1'
                for i, item in enumerate(items):
                    if 'm²' in item:
                        meters = items[i-1]
                loader.add_value('meters', meters)

                yield loader.load_item()
                # i += 1
            next_page = response.css('li.next a::attr(href)').get()
            print('entrando a ', next_page)
            if next_page is not None and '10' not in next_page:
                yield response.follow(next_page, callback=self.parsear, errback=self.handle_errors, meta=response.meta)
                pass

        except Exception as e:
            print('error ', str(e))

    def fallao(self, response):
        print('fallao')
        print(response)

    def handle_errors(self, failure):
        print('fallao')
        print(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            print('HttpError on ' + response.url)
            if response.status == 403:
                print('Error 403, access denied')
                if response.meta['retries'] < MAX_RETRIES:
                    response.meta['retries'] += 1
                    try:
                        print('Retry N°{} on {}'.format(response.meta['retries'], response.url))
                        yield response.follow(response.url, callback=self.parsear, errback=self.handle_errors,
                                              meta=response.meta, dont_filter=True)
                        #yield Request(response.url, callback=self.parsear, errback=self.handle_errors, dont_filter=True)
                    except:
                        print('no se pudo')
                else:
                    print('Exiting, max retries reached')

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            print('DNSLookupError on ' + request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            print('TimeoutError on ' + request.url)

