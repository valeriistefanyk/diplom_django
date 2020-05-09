# Generated by Django 3.0.4 on 2020-05-09 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True)),
                ('telephone1', models.CharField(blank=True, default='', max_length=15)),
                ('telephone2', models.CharField(blank=True, default='', max_length=15)),
                ('avatar', models.ImageField(blank=True, upload_to='employees')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
