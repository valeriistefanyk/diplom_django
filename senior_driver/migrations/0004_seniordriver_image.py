# Generated by Django 3.0.4 on 2020-03-19 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('senior_driver', '0003_auto_20200315_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='seniordriver',
            name='image',
            field=models.ImageField(blank=True, upload_to='employees'),
        ),
    ]