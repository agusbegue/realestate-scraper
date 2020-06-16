# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import Request, Response

from scrapy_app.items import PostItem
from scrapy_app.settings import MAX_RETRIES
from main.models import ScrapyJob, FINISHED, RUNNING


class IdealistaSpider(CrawlSpider):
    name = 'idealista'
    base_url = 'https://idealista.com'
    allowed_domains = [base_url]

    def __init__(self, *args, **kwargs):
        self.job_task = kwargs.get('_job')
        ScrapyJob.objects.filter(task=self.job_task).update(status=RUNNING)
        #self.url = kwargs.get('url')
        self.start_url = 'https://www.idealista.com/point/venta-viviendas/36.71643/-4.30017/17/mapa-google'
        self.post_count = 0
        self.http_status = 200

        IdealistaSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(IdealistaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.distribute_crawling,
                      errback=self.handle_errors, meta={'retries': 0})

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
                #self.parsear(response)
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

                loader.add_value('job_task', self.job_task)
                self.post_count += 1
                yield loader.load_item()

        except Exception as e:
            print('error ', str(e))

    def handle_errors(self, failure):
        response = failure.value.response
        if response.status == 403:
            print('Error 403, access denied')
            if response.meta['retries'] < MAX_RETRIES:
                response.meta['retries'] += 1
                yield Request(response.url, callback=self.parsear, errback=self.handle_errors,
                              meta=response.meta, dont_filter=True)
            else:
                print('max retries')
        print('status', response.status)
        self.http_status = response.status

    def close(self, reason):
        ScrapyJob.objects.filter(task=self.job_task).update(status=FINISHED,
                                                            post_count=self.post_count,
                                                            http_status=self.http_status)


