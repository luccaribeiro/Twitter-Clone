# Generated by Django 4.0.6 on 2022-07-28 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_alter_retweet_options_alter_tweet_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='capa',
            field=models.ImageField(default='default.jpg', upload_to='background_images'),
        ),
    ]
