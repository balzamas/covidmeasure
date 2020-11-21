# Generated by Django 3.0.5 on 2020-11-21 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measuremeterdata', '0067_auto_20201121_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='chcases',
            name='r0low',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=17, null=True),
        ),
        migrations.AddField(
            model_name='chcases',
            name='r0median',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=17, null=True),
        ),
        migrations.AddField(
            model_name='chcases',
            name='r0peak',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=17, null=True),
        ),
    ]
