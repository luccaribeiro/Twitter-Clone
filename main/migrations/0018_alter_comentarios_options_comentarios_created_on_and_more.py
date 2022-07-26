# Generated by Django 4.0.6 on 2022-07-18 18:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_comentarios'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentarios',
            options={'ordering': ['created_on']},
        ),
        migrations.AddField(
            model_name='comentarios',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='comentarios',
            name='tweet',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comentarios',
                to='main.tweet'),
        ),
    ]
