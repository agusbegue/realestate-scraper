import json
from django.db.models import Field, Model, CharField, AutoField, IntegerField, BooleanField, URLField
# from scrapy_app.scrapy_app.items import ScrapyItem
from django.utils import timezone
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)


class Post(Model):
    # def __init__(self, name=None, price=None):
    #     self.name = name
    #     self.price = price
    id = IntegerField(primary_key=True)
    # id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    price = IntegerField()
    link = URLField(default='idealista.com')
    meters = IntegerField()
    new = BooleanField(default=True)
