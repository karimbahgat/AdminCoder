# Generated by Django 3.2.11 on 2022-11-13 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminImporter', '0002_datasetimporter_import_params_new'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datasetimporter',
            old_name='import_params',
            new_name='import_params_old',
        ),
    ]
