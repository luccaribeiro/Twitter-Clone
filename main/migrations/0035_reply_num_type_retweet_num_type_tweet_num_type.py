# Generated by Django 4.0.6 on 2022-07-28 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_profile_capa'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='num_type',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='retweet',
            name='num_type',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='tweet',
            name='num_type',
            field=models.IntegerField(default=0),
        ),
    ]