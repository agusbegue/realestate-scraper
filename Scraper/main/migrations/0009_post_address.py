# Generated by Django 3.0.4 on 2020-08-14 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_post_distance'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='address',
            field=models.CharField(default='aaa', max_length=100),
            preserve_default=False,
        ),
    ]
