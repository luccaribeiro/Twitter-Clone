# Generated by Django 4.0.6 on 2022-07-13 17:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
