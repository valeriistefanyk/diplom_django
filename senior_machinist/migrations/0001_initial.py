# Generated by Django 3.0.4 on 2020-05-09 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('machines', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('engineer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeniorMachinist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brigade_name', models.CharField(blank=True, max_length=50)),
                ('telephone1', models.CharField(blank=True, default='', max_length=30)),
                ('telephone2', models.CharField(blank=True, default='', max_length=30)),
                ('avatar', models.ImageField(blank=True, default='no-image.png', upload_to='employees')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_start_work', models.DateField(blank=True, null=True)),
                ('machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='machines.Machine')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TempReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_completion', models.DateTimeField(auto_now_add=True)),
                ('updated_data', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(unique=True)),
                ('checked', models.BooleanField(blank=True, default=False)),
                ('stage', models.CharField(choices=[('no', 'Пустий звіт'), ('strt', 'Початок створення'), ('part', 'Частично заповнений'), ('full', 'Заповнений'), ('fwdi', 'Відісланий інженеру'), ('chki', 'Звіт перевірений інженером'), ('fwdd', 'Відісланий директору'), ('chkd', 'Звіт перевірений директором')], default='no', max_length=4)),
                ('motohour', models.FloatField(blank=True, null=True)),
                ('km', models.FloatField(blank=True, null=True)),
                ('fuel', models.FloatField(blank=True, null=True)),
                ('maslo', models.FloatField(blank=True, null=True)),
                ('breakage', models.BooleanField(default=False)),
                ('breakage_info', models.TextField(blank=True, null=True)),
                ('breakage_date_start', models.DateField(blank=True, null=True)),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='engineer.Engineer')),
                ('filled_up', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='senior_machinist.SeniorMachinist')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machines.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='MotoAndFuelInfoReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motohour_before', models.FloatField(blank=True, null=True)),
                ('motohour_after', models.FloatField(blank=True, null=True)),
                ('km_before', models.FloatField(blank=True, null=True)),
                ('km_after', models.FloatField(blank=True, null=True)),
                ('info', models.CharField(blank=True, max_length=200, null=True)),
                ('report', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='senior_machinist.TempReport')),
            ],
        ),
        migrations.CreateModel(
            name='MasloInfoReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marka', models.CharField(blank=True, max_length=30, null=True)),
                ('vidano', models.CharField(blank=True, max_length=30)),
                ('maslo_before', models.FloatField(blank=True, null=True)),
                ('maslo_after', models.FloatField(blank=True, null=True)),
                ('info', models.CharField(blank=True, max_length=200, null=True)),
                ('report', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='senior_machinist.TempReport')),
            ],
        ),
        migrations.CreateModel(
            name='MachineWorkingReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(blank=True, max_length=20, null=True)),
                ('station_from', models.CharField(blank=True, max_length=50, null=True)),
                ('station_to', models.CharField(blank=True, max_length=50, null=True)),
                ('departure_time', models.DateTimeField(blank=True, null=True)),
                ('arrival_time', models.DateTimeField(blank=True, null=True)),
                ('latFld', models.FloatField(blank=True, null=True)),
                ('lngFld', models.FloatField(blank=True, null=True)),
                ('time_from', models.DateTimeField(blank=True, null=True)),
                ('time_to', models.DateTimeField(blank=True, null=True)),
                ('place_working', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('workday_production', models.CharField(blank=True, max_length=50, null=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='senior_machinist.TempReport')),
            ],
        ),
        migrations.CreateModel(
            name='BrigadeMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('telephone1', models.CharField(blank=True, default='', max_length=30)),
                ('telephone2', models.CharField(blank=True, default='', max_length=30)),
                ('job_title', models.CharField(choices=[('hlp', 'допоможний персонал'), ('mnst', 'машиніст')], default='mnst', max_length=4)),
                ('seniormachinist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='senior_machinist.SeniorMachinist')),
            ],
        ),
        migrations.CreateModel(
            name='BrigadeInfoReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_from', models.DateTimeField(blank=True, null=True)),
                ('date_time_to', models.DateTimeField(blank=True, null=True)),
                ('medical_check_before', models.CharField(choices=[('na', 'не допущенний'), ('al', 'допущений'), ('hl', 'здоровий'), ('ps', 'пройдено'), ('uk', 'невідомо')], default='uk', max_length=2)),
                ('medical_check_after', models.CharField(choices=[('na', 'не допущенний'), ('al', 'допущений'), ('hl', 'здоровий'), ('ps', 'пройдено'), ('uk', 'невідомо')], default='uk', max_length=2)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='senior_machinist.BrigadeMembers')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='senior_machinist.TempReport')),
            ],
        ),
    ]
