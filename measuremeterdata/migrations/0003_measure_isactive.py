# Generated by Django 3.0.5 on 2020-04-29 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measuremeterdata', '0002_auto_20200429_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='measure',
            name='isactive',
            field=models.BooleanField(default=True),
        ),
    ]
