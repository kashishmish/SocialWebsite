# Generated by Django 3.1.2 on 2021-05-04 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_reaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation', models.IntegerField()),
                ('email_reciever', models.CharField(max_length=100)),
                ('email_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.registration')),
            ],
        ),
    ]
