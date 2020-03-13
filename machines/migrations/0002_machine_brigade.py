# Generated by Django 3.0.4 on 2020-03-13 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('senior_driver', '0002_seniordriver_brigade_name'),
        ('machines', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='brigade',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='senior_driver.SeniorDriver'),
            preserve_default=False,
        ),
    ]
