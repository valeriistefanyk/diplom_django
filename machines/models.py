from django.db import models
from senior_driver.models import SeniorDriver

class Machine(models.Model):
    """Опис колійних машин"""
    
    inventory_number = models.IntegerField()
    name = models.CharField(max_length=40)
    number_machine = models.IntegerField()
    year_of_commissioning = models.DateField()
    
    engine_brand = models.CharField(max_length=50, default=None, blank=True)
    engine_number = models.CharField(max_length=50, blank=True, default=None)
    capacity = models.FloatField(blank=True, default=None)
    costs_at_rate = models.FloatField(blank=True, default=None)
    dizmaslo = models.FloatField(blank=True, default=None)

    turbocharger_mark = models.CharField(max_length=50, blank=True, default=None)
    turbocharger_count = models.SmallIntegerField(blank=True, default=None)

    filtr_air = models.CharField(max_length=6, blank=True, default=None)
    filtr_fuel = models.CharField(max_length=6, blank = True, default=None)
    filtr_dizmaslo = models.CharField(max_length=6, blank=True, default=None)
    filtr_gidravlichni = models.CharField(max_length=6, blank = True, default=None)

    lining_blocks_mark = models.CharField(max_length=30, blank=True)
    lining_blocks_count = models.SmallIntegerField(blank=True)
    lining_pidpiiki_mark = models.CharField(max_length=30, blank=True)
    lining_pidpiiki_count = models.CharField(max_length=30, blank=True)

    compressor_mark = models.CharField(max_length=30, blank=True)
    compressor_count = models.SmallIntegerField(blank=True)

    diametr_wheel_pairs = models.CharField(max_length=30, blank=True, default=None)

    battery_kind = models.CharField(max_length=40, blank=True)
    battery_count = models.CharField(max_length=30, blank=True)
    battery_last_replacement = models.CharField(max_length=50, blank=True)
    battery_count_need = models.CharField(max_length=10, blank=True)

    date_ost_kr = models.DateField(blank=True, null=True)
    initial_value = models.FloatField(blank=True, default=None)
    residual_value = models.FloatField(blank=True, default=None)
    depreciation_end_date = models.DateField()

    dizmaslo_mark = models.CharField(max_length=20)
    dizmaslo_volume = models.IntegerField()

    transmission_fluid_mark = models.CharField(max_length=100, blank=True)
    transmission_fluid_volume = models.IntegerField(blank=True)
    
    hydraulic_fluid_mark = models.CharField(max_length=100, blank=True)
    hydraulic_fluid_volume = models.CharField(max_length=30, blank=True)

    brigade = models.ForeignKey(SeniorDriver, on_delete=models.CASCADE)


    def full_name(self):
        return f"{self.name} №{self.number_machine} [IN {self.inventory_number}]" 

    def __str__(self):
        return f"{self.name} № {self.number_machine} [{self.inventory_number}]"

    # district = models.ForeignKey(Brigade, null = True, on_delete=models.CASCADE)
