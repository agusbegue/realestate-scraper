# Generated by Django 3.0.4 on 2020-08-14 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200813_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='distance',
            field=models.IntegerField(default=150),
            preserve_default=False,
        ),
    ]