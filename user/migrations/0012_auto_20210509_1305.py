# Generated by Django 3.1.2 on 2021-05-09 07:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20210509_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addpost',
            name='datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 9, 13, 5, 20, 973883)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 9, 13, 5, 20, 973883)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='message',
            field=models.CharField(max_length=500),
        ),
    ]
