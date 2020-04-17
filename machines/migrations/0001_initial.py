# Generated by Django 3.0.4 on 2020-04-17 15:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('senior_driver', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_number', models.CharField(max_length=50)),
                ('number_machine', models.CharField(max_length=30)),
                ('year_of_commissioning', models.DateField(blank=True, null=True)),
                ('rated_capacity', models.FloatField(blank=True, null=True)),
                ('costs_at_rate', models.FloatField(blank=True, null=True)),
                ('dizmaslo', models.FloatField(blank=True, null=True)),
                ('diametr_wheel_pairs', models.CharField(blank=True, max_length=30, null=True)),
                ('date_ost_kr', models.DateField(blank=True, null=True)),
                ('initial_value', models.FloatField(blank=True, null=True)),
                ('residual_value', models.FloatField(blank=True, null=True)),
                ('depreciation_end_date', models.DateField(blank=True, null=True)),
                ('breakage', models.BooleanField(default=False)),
                ('breakage_date', models.DateField(blank=True, null=True)),
                ('breakage_info', models.TextField(blank=True, null=True)),
                ('work_days', models.IntegerField(default=0)),
                ('last_used_data', models.DateField(default=datetime.date(2009, 10, 5))),
                ('brigade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='senior_driver.SeniorDriver')),
            ],
        ),
        migrations.CreateModel(
            name='MachineName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default='')),
                ('image', models.ImageField(blank=True, upload_to='machines')),
            ],
        ),
        migrations.CreateModel(
            name='Turbocharger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=30, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turbochargers', to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='TransmissionFluid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=50, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transmission_fluid', to='machines.Machine')),
            ],
        ),
        migrations.AddField(
            model_name='machine',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machines.MachineName'),
        ),
        migrations.CreateModel(
            name='LiningPidpiiki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=30, null=True)),
                ('count', models.CharField(blank=True, max_length=10, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pidpiikies', to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='LiningBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=30, null=True)),
                ('count', models.SmallIntegerField(blank=True, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='HydraulicFluid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=50, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hydraulic_fluid', to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('air', models.CharField(blank=True, max_length=50, null=True)),
                ('fuel', models.CharField(blank=True, max_length=50, null=True)),
                ('dizmaslo', models.CharField(blank=True, max_length=50, null=True)),
                ('gidravlichni', models.CharField(blank=True, max_length=50, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=30, null=True)),
                ('number', models.CharField(blank=True, max_length=30, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engines', to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Dizmaslo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=50, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dizmaslos', to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Compressor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=30, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compressors', to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Battery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empty', models.BooleanField(default=False)),
                ('marka', models.CharField(blank=True, max_length=40, null=True)),
                ('count', models.CharField(blank=True, max_length=30, null=True)),
                ('last_replacement', models.DateField(blank=True, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batteries', to='machines.Machine')),
            ],
        ),
    ]
