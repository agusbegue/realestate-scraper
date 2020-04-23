# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import Request, Response
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from scrapy_app.items import PostItem
from scrapy_app.settings import MAX_RETRIES, POSTS_PER_PAGE

class IpCheck(CrawlSpider):
    name = 'ipcheck'
    start_urls = ['https://www.whatismyip.com/']

    def start_requests(self):
        print('entrando a ', self.start_urls[0])
        yield Request(self.start_urls[0], callback=self.parsear)

    def parsear(self, response):
        print('entro a ', response.url)
        response.css('div.card-body')


class IdealistaSpider(CrawlSpider):
    name = 'idealista'
    base_url = 'https://idealista.com'
    allowed_domains = [base_url]
    #start_urls = ['https://www.idealista.com/venta-viviendas/barcelona-barcelona/']
    #start_urls = ['https://www.idealista.com/venta-viviendas/barcelona-barcelona/con-metros-cuadrados-mas-de_95,metros-cuadrados-menos-de_100/']

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.start_urls = [self.base_url + self.url]

        IdealistaSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(IdealistaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        print('entro start_reqs', self.start_urls)
        yield Request(url=self.start_urls[0], callback=self.distribute_crawling, errback=self.handle_errors, meta={'retries': 0})

    #pudo entrar a parsear desde handle_errors pero no desde aca, wtf
    def distribute_crawling(self, response):
        print('entro distrib')
        try:
            texto = response.css('h1.listing-title::text').getall()[1].strip()
            cantidad_posts = int(texto[:texto.find(' ')].replace('.', ''))
            if cantidad_posts > 0:
                # n_pages = int((cantidad_posts - 1)/POSTS_PER_PAGE) + 1
                n_pages = 5
                print('crawling {} pages'.format(n_pages))
                pages_list = ['pagina-{}.htm'.format(i) for i in range(2, n_pages+1)]
                #creo que esto no esta andando
                self.parsear(response)
                for page in [''] + pages_list:
                    print('entering url ', response.url + page)
                    yield Request(response.url + page, callback=self.parsear, errback=self.handle_errors,
                                  meta={'retries': 0}, dont_filter=True)
        except Exception as e:
            print('Problem extracting N° posts: ', str(e))

    def parsear(self, response):
        print('entro a {}'.format(response.url))
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
            # next_page = response.css('li.next a::attr(href)').get()
            # print('entrando a ', next_page)
            # if next_page is not None and '10' not in next_page:
            #     yield response.follow(next_page, callback=self.parsear, errback=self.handle_errors, meta=response.meta)
            #     pass

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
                        yield Request(response.url, callback=self.parsear, errback=self.handle_errors,
                                      meta=response.meta, dont_filter=True)
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

