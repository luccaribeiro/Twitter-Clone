# Generated by Django 4.0.6 on 2022-07-27 20:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_remove_tweet_reply_to_alter_like_date_reply'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterField(
            model_name='like',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 7, 27, 20, 21, 11, 867965, tzinfo=utc)),
        ),
    ]
