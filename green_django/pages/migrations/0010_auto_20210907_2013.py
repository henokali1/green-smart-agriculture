# Generated by Django 3.2.5 on 2021-09-07 20:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_alter_sensorhisdata_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorhisdata',
            name='ts',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sensorhisdata',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
