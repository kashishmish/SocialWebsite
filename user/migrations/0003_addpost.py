# Generated by Django 3.1.2 on 2021-05-03 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210501_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addpost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='post')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('like', models.IntegerField(max_length=100)),
                ('dislike', models.IntegerField(max_length=100)),
            ],
        ),
    ]
