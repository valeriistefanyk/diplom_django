# Generated by Django 3.0.4 on 2020-04-25 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineer', '0005_auto_20200419_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinereport',
            name='latFld',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='machinereport',
            name='lngFld',
            field=models.FloatField(blank=True, null=True),
        ),
    ]