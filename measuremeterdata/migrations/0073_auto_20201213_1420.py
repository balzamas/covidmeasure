# Generated by Django 3.0.5 on 2020-12-13 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measuremeterdata', '0072_auto_20201205_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chmeasure',
            name='level',
            field=models.IntegerField(choices=[(-1, 'Relaxed'), (0, 'CH Level'), (1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4')], default=0),
        ),
    ]
