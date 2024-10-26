# Generated by Django 5.0.1 on 2024-04-16 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_photo_user_alter_comment_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 15, 53, 21, 634681)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 15, 53, 21, 634681)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=models.CharField(default='<function uuid4 at 0x000002B4E7A5CEA0>', max_length=128, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
