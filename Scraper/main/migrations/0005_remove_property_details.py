# Generated by Django 3.0.4 on 2020-07-31 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_scrapyjob_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='details',
        ),
    ]
