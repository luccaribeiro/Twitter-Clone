# Generated by Django 4.0.6 on 2022-07-15 17:23

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_profile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(default={django.contrib.auth.models.User}, max_length=160),
        ),
    ]
