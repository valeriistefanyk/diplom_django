# Generated by Django 3.0.4 on 2020-03-13 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('senior_driver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seniordriver',
            name='brigade_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]