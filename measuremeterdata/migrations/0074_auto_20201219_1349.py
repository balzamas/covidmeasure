# Generated by Django 3.0.5 on 2020-12-19 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuremeterdata', '0073_auto_20201213_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chdeaths',
            old_name='average_deaths',
            new_name='average_deaths_15_19',
        ),
        migrations.RenameField(
            model_name='chdeaths',
            old_name='deaths',
            new_name='deaths20',
        ),
    ]
