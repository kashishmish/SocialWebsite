# Generated by Django 3.1.2 on 2021-05-03 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_addpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addpost',
            name='dislike',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='addpost',
            name='like',
            field=models.IntegerField(),
        ),
    ]
