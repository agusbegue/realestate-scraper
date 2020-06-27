import json
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.validators import ValidationError
from django.contrib.auth.models import AbstractUser

from scrapyd_api import ScrapydAPI

from main.settings import SCRAPYD_URL, MAX_FILE_SIZE
from main.excel import FileReader, FileCreator
from main import constants as c


class User(AbstractUser):

    email = models.EmailField('Email address', unique=True, null=False)
    REQUIRED_FIELDS = ['email']


class ScrapyJob(models.Model):

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, default=c.PENDING)
    task = models.CharField(max_length=25, default=c.NOT_DEFINED)
    details = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(default=timezone.now)
    records = models.IntegerField(null=True)
    http_status = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def start(self, file):
        reader = FileReader(self)
        properties = reader.read(file)
        self._send()
        self.save()
        if properties:
            self._save_properties(properties)

    def cancel(self):
        if not self.is_done:
            # scrapyd = ScrapydAPI(SCRAPYD_URL)
            # scrapyd.cancel('default', self.task)
            pass

    def to_file(self):
        props = Property.objects.filter(job_id=self.id)
        creator = FileCreator(props, bulk=True)
        return creator.get_data()

    def _send(self):
        scrapyd = ScrapydAPI(SCRAPYD_URL)
        self.task = '012345' # scrapyd.schedule('default', 'idealista', job_key=self.id)

    def _save_properties(self, properties):
        for data in properties:
            prop = Property(**data)
            prop.job_id = self.id
        Property.objects.bulk_create(properties)

    @property
    def row_color(self):
        if self.status == 'Pending' or self.status == 'Running':
            return 'LightYellow'
        elif self.status == 'Failed':
            return 'LightCoral'
        else:
            return 'PaleGreen'

    @property
    def is_done(self):
        return self.status == c.FINISHED


class Property(models.Model):

    type = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    surface = models.FloatField()
    parking = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    job = models.ForeignKey(ScrapyJob, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    def clean(self):
        if False:
            raise ValidationError('Incorrect field format')
        elif False:
            raise SyntaxError('Blank fields')

    def to_file(self):
        creator = FileCreator(self, bulk=False)
        return creator.get_data()

    @property
    def row_color(self):
        if self.done:
            return 'PaleGreen'
        elif self.valid:
            return 'LightYellow'
        else:
            return 'LightCoral'


class Statistics(models.Model):

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    price = models.FloatField()


class UserData(models.Model):
    pass


