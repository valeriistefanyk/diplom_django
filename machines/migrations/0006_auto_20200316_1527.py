# Generated by Django 3.0.4 on 2020-03-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0005_machinename_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinename',
            name='image',
            field=models.ImageField(blank=True, upload_to='machines'),
        ),
    ]
