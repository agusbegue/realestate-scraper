import json
from django.utils import timezone
from django.db.models import CASCADE, Model, CharField, AutoField, ForeignKey, URLField, FloatField, DateTimeField, IntegerField
from scrapyd_api import ScrapydAPI
from main.settings import SCRAPYD_URL

NOT_DEFINED = 'not defined'
PENDING = 'pending'
RUNNING = 'running'
FINISHED = 'finished'
ERROR = 'error'


class ScrapyJob(Model):

    id = AutoField(primary_key=True)
    status = CharField(max_length=10, default=PENDING)
    task = CharField(max_length=25, default=NOT_DEFINED)
    scraped_url = URLField(max_length=40, default=NOT_DEFINED)
    details = CharField(max_length=50, default=NOT_DEFINED)
    date = DateTimeField(default=timezone.now, blank=True)
    post_count = IntegerField(default=0)
    http_status = IntegerField(default=0)

    def send(self, categoria, lugar):
        scrapyd = ScrapydAPI(SCRAPYD_URL)
        self.scraped_url = '/venta-{}/{}/'.format(categoria, lugar)
        self.task = scrapyd.schedule('default', 'idealista', url=self.scraped_url, job_key=self.id)
        self.save()
        #ScrapyJob.objects.filter(id=self.id).update(**self.__data__())

    @classmethod
    def update_jobs(cls):
        scrapyd = ScrapydAPI(SCRAPYD_URL)
        for job in cls.objects.exclude(status=FINISHED):
            new_status = scrapyd.job_status('default', job.task)
            if new_status == '' and job.status == PENDING:
                cls.objects.filter(pk=job.id).update(status=ERROR)
            elif new_status != job.status and new_status != '':
                cls.objects.filter(pk=job.id).update(status=new_status)
        return len(cls.objects.exclude(status=FINISHED)) == 0

    def __data__(self):
        data = self.__dict__
        data.pop('_state')
        return data

    #def __str__(self):
    #    return


class Post(Model):

    id = AutoField(primary_key=True)
    name = CharField(max_length=150)
    price = FloatField(default=-1)
    link = URLField(default='idealista.com')
    meters = FloatField(default=-1)
    job_task = CharField(max_length=50, default=NOT_DEFINED)
    job = ForeignKey(ScrapyJob, on_delete=CASCADE, null=True, blank=True)
    ratio = FloatField(default=-1)

    def save(self, *args, **kwargs):
        try:
            self.ratio = round(self.price / self.meters, 2)
            self.job = ScrapyJob.objects.filter(task=self.job_task)[0]
        except ZeroDivisionError:
            pass
        except IndexError:
            pass
        finally:
            super().save(*args, **kwargs)
