# Generated by Django 4.0.6 on 2022-07-18 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_comentarios_tweet'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentarios',
            options={'ordering': ['-created_on']},
        ),
    ]
