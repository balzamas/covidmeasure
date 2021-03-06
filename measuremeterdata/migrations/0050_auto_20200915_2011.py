# Generated by Django 3.0.5 on 2020-09-15 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measuremeterdata', '0049_remove_country_mapcode_europe'),
    ]

    operations = [
        migrations.AddField(
            model_name='casesdeaths',
            name='positivity',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='casesdeaths',
            name='cases_past14days',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='casesdeaths',
            name='cases_past7days',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='casesdeaths',
            name='cases_per_mio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='casesdeaths',
            name='cases_per_mio_seven',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='casesdeaths',
            name='deaths_past14days',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='casesdeaths',
            name='deaths_per100k',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='casesdeaths',
            name='deaths_total_per100k',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True),
        ),
    ]
