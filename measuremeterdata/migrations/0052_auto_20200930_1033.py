# Generated by Django 3.0.5 on 2020-09-30 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuremeterdata', '0051_auto_20200930_0919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chcases',
            old_name='cases_past10days',
            new_name='incidence_past10days',
        ),
        migrations.RenameField(
            model_name='chcases',
            old_name='cases_past14days',
            new_name='incidence_past14days',
        ),
        migrations.RenameField(
            model_name='chcases',
            old_name='cases_past7days',
            new_name='incidence_past7days',
        ),
    ]
