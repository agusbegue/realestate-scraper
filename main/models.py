from requests import post
from requests.exceptions import ConnectionError as RequestsConnectionError

from django.utils import timezone
from django.db import models
from django.core.validators import ValidationError
from django.contrib.auth.models import AbstractUser

from main.utils.excel import FileReader, FileCreator
from main.utils import constants as c
from telegram_bot.errors import report_error


class User(AbstractUser):

    email = models.EmailField('Email address', unique=True, null=False)
    REQUIRED_FIELDS = ['email']


class ScrapyJob(models.Model):

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, default=c.PENDING)
    details = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(default=timezone.now)
    records = models.IntegerField(null=True)
    http_status = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def start(self, file):
        reader = FileReader(self)
        properties = reader.read(file)
        self.save()
        if properties:
            self._save_properties(properties)
            self._send()

    def to_file(self):
        props = self.property_set.prefetch_related('post_set').all()
        creator = FileCreator(props)
        return creator.get_data()

    def _send(self):
        failed = False
        try:
            r = post(f'http://localhost:6800/schedule.json?project=default&spider=idealista&job_id={self.id}')
            if r.status_code != 200:
                failed = True
        except RequestsConnectionError:
            failed = True

        if failed:
            self.status = c.FAILED
            self.save()
            report_error(self.user.username, 'Connection Error: Scrapyd server not available')

    def _save_properties(self, properties):
        prop_objects = []
        for data in properties:
            prop = Property(**data)
            prop.job_id = self.id
            prop_objects.append(prop)
        Property.objects.bulk_create(prop_objects)

    @property
    def row_color(self):
        if self.status == 'Pending' or self.status == 'Running':
            return 'LightYellow'
        elif self.status == 'Failed':
            return 'Pink'
        else:
            return 'HoneyDew'

    @property
    def is_done(self):
        return self.status == c.FINISHED or self.status == c.FAILED


class Property(models.Model):

    job = models.ForeignKey(ScrapyJob, on_delete=models.CASCADE)

    type = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    area = models.FloatField()
    parking = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()

    valid = models.BooleanField(default=True)
    done = models.BooleanField(default=False)

    avg_price = models.FloatField(null=True)
    radius = models.IntegerField(null=True)

    def clean(self):
        if False:
            raise ValidationError('Incorrect field format')
        elif False:
            raise SyntaxError('Blank fields')

    def to_file(self):
        creator = FileCreator([self])
        return creator.get_data()

    def get_posts(self):
        return self.post_set.all()

    @property
    def row_color(self):
        if self.done:
            return 'HoneyDew'
        elif self.valid:
            return 'LightYellow'
        else:
            return 'Pink'

    @property
    def get_price(self):
        if self.avg_price:
            return '€ ' + str(self.avg_price)
        return ''


class Post(models.Model):

    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    index = models.IntegerField()
    link = models.URLField()
    price = models.FloatField()
    area = models.FloatField()
    address = models.CharField(max_length=100)
    distance = models.IntegerField()

    @property
    def get_index(self):
        if self.index:
            return str(self.index) + '°'
        return ''

    @property
    def get_link(self):
        if self.link:
            return 'https://idealista.com' + str(self.link)
        return '#'


class UserData(models.Model):
    pass


