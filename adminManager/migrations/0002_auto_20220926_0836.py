# Generated by Django 3.2.4 on 2022-09-26 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='maxx',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='maxy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='minx',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='miny',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
