# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy_app.items import PostItem
from scrapy.http import Request, Response


class IdealistaSpider(CrawlSpider):
    name = 'idealista'
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
        yield Request(url=self.start_urls[0], callback=self.parse, errback=self.parse_fail)

    def parse(self, response):
        print('entro', response.url)
        try:
            posts = response.css('article.item')
            for post in posts:
                loader = ItemLoader(item=PostItem(), selector=post)
                # loader.add_value('id', i)
                loader.add_value('name', post.css('.item-link::text').get()),
                loader.add_value('price', post.css('.item-price::text').get())
                loader.add_value('link', post.css('.item-link a::attr(href)').get())
                # print(post.css('a::attr(href)').get())
                loader.add_value('meters', post.css('.item-detail')[1].css('::text').get())
                yield loader.load_item()
                # i += 1
            # next_page = response.css('li.next a').get()
            # print('aa', next_page)
            # if next_page is not None:
            #    print('bb')
            #    print(next_page)
            #    yield response.follow(next_page, callback=self.parse)

            #for a in response.css('a.icon-arrow-right-after::attr(href)').get():
            #    print(a)
            #    yield response.follow(a, callback=self.parse)
        except Exception as e:
            print('error ', str(e))

        ''' otra opcion
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
        '''

    def parse_fail(self, response):
        print('fallao')
        print(response)