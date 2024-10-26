# Generated by Django 5.0.1 on 2024-04-11 16:25

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.CharField(max_length=32)),
                ('user', models.CharField(max_length=32)),
                ('text', models.TextField(max_length=1024)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2024, 4, 11, 22, 25, 5, 439353))),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['text'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100, verbose_name='Source')),
                ('filter', models.CharField(choices=[(0, 'no'), (1, 'lofi'), (2, 'brooklyn'), (3, 'gingham'), (4, 'valencia'), (5, 'willow')], default=(0, 'no'), max_length=16, verbose_name='Filter')),
                ('likes', models.IntegerField(default=0, verbose_name='Likes')),
                ('dislikes', models.IntegerField(default=0, verbose_name='Dislikes')),
                ('text', models.TextField(blank=True, max_length=1024)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2024, 4, 11, 22, 25, 5, 438354))),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
                'ordering': ['text'],
            },
        ),
    ]
