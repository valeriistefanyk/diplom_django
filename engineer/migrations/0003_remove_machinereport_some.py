# Generated by Django 3.0.4 on 2020-04-19 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engineer', '0002_machinereport_some'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machinereport',
            name='some',
        ),
    ]
