# Generated by Django 3.0.4 on 2020-03-15 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('senior_driver', '0002_seniordriver_brigade_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='seniordriver',
            name='telephone1',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
        migrations.AddField(
            model_name='seniordriver',
            name='telephone2',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
    ]