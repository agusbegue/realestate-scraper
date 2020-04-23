import json
from django.db.models import Field, Model, CharField, AutoField, IntegerField, BooleanField, URLField, FloatField
from scrapyd_api import ScrapydAPI


NOT_DEFINED = 'not defined'

class Post(Model):
    # id = IntegerField(primary_key=True)
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    price = IntegerField(default=-1)
    link = URLField(default='idealista.com')
    meters = IntegerField(default=-1)
    new = BooleanField(default=True)
    ratio = FloatField(default=-1)

    def save(self, *args, **kwargs):
        try:
            self.ratio = round(self.price / self.meters, 2)
        except:
            pass
        finally:
            super().save(*args, **kwargs)


class ScrapyJob(Model):

    id = AutoField(primary_key=True)
    status = CharField(max_length=10, choices=((0, 'pending'), (1, 'running'), (2, 'finished')), default='pending')
    api_url = CharField(max_length=20, default='http://localhost:6800')
    task = CharField(max_length=25, default=NOT_DEFINED)
    scraped_url = URLField(max_length=40, default=NOT_DEFINED)
    details = CharField(max_length=50, default=NOT_DEFINED)

    def __init__(self, api_url, *args, **kwargs):
        self.api_url = api_url
        super().__init__(*args, **kwargs)
        self.save()

    def start(self, categoria, lugar):
        scrapyd = ScrapydAPI(self.api_url)
        self.scraped_url = '/venta-{}/{}/'.format(categoria, lugar)
        self.task = scrapyd.schedule('default', 'idealista', url=self.scraped_url)
        self.status = 'running'
        ScrapyJob.objects.filter(id=self.id).update(**self.__data__())

    def __data__(self):
        data = self.__dict__
        data.pop('_state')
        return data
