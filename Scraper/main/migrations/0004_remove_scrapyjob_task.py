# Generated by Django 3.0.4 on 2020-07-30 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200730_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapyjob',
            name='task',
        ),
    ]