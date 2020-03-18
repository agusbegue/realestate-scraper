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

    def parse(self, response):
        try:
            posts = response.css('article.item')
            i = 1
            for post in posts:
                loader = ItemLoader(item=PostItem(), selector=post)
                loader.add_value('id', i)
                loader.add_value('name', post.css('.item-link::text').get()),
                loader.add_value('price', post.css('.item-price::text').get())
                loader.add_value('link', post.css('.item-link a::attr(href)').get())
                # print(post.css('a::attr(href)').get())
                items = post.css('.item-detail')
                for item in items:
                    clave = item.css('small::text').get()
                    print('======'+clave+'================')
                    print('m' in clave)
                    if 'm' in clave and '2' in clave:
                        print('___entro____')
                        loader.add_value('meters', item.css('::text').get())

                i += 1
                yield loader.load_item()
        except Exception as e:
            print(str(e))

        ''' otra opcion
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
        '''
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_fail(self, response):
        pass

