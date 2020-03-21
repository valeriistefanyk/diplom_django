# Generated by Django 3.0.4 on 2020-03-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0014_auto_20200321_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='battery_count',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='battery_count_need',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='battery_kind',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='battery_last_replacement',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='compressor_count',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='compressor_mark',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='dizmaslo_mark',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='dizmaslo_volume',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='engine_brand',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='engine_number',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='filtr_air',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='filtr_dizmaslo',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='filtr_fuel',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='filtr_gidravlichni',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='hydraulic_fluid_mark',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='hydraulic_fluid_volume',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='lining_blocks_count',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='lining_blocks_mark',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='lining_pidpiiki_count',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='lining_pidpiiki_mark',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='transmission_fluid_mark',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='transmission_fluid_volume',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='turbocharger_count',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='turbocharger_mark',
        ),
        migrations.AlterField(
            model_name='battery',
            name='empty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='compressor',
            name='empty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dizmaslo',
            name='empty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='filter',
            name='empty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hydraulicfluid',
            name='empty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='liningblock',
            name='empty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='liningpidpiiki',
            name='empty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transmissionfluid',
            name='empty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='turbocharger',
            name='empty',
            field=models.BooleanField(default=False),
        ),
    ]
