from django.db import models
from senior_driver.models import SeniorDriver
import datetime

class Machine(models.Model):
    """Опис колійних машин"""
    
    machine = models.ForeignKey('MachineName', on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50, blank=True, null=True)

    inventory_number = models.CharField(max_length=50)
    number_machine = models.CharField(max_length=30)
    year_of_commissioning = models.DateField(blank=True, null=True)
    
    rated_capacity = models.FloatField(blank=True, null=True)
    costs_at_rate = models.FloatField(blank=True, null=True)
    dizmaslo = models.FloatField(blank=True, null=True)
    diametr_wheel_pairs = models.CharField(max_length=30, blank=True, null=True)

    date_ost_kr = models.DateField(blank=True, null=True)
    initial_value = models.FloatField(blank=True, null=True)
    residual_value = models.FloatField(blank=True, null=True)
    depreciation_end_date = models.DateField(blank=True, null=True)

    breakage = models.BooleanField(default=False)
    breakage_date = models.DateField(blank=True, null=True)
    breakage_info = models.TextField(blank=True, null=True)
    fix_date = models.DateField(blank=True, null=True)
    fix_by = models.CharField(max_length=50, blank=True, null=True)

    NORMAL = '0'
    CALLENGINEER = '1'
    DNTRUSH = '2'
    SCRITICAL = '3'
    VCRITICAL = '4'
    UNKNOW = '5'
    MACHINE_STATUS = [
        (VCRITICAL, 'Дуже критичний, потребує терміновий ремонт'),
        (SCRITICAL, 'Потребує капітального ремонту'),
        (DNTRUSH, 'Не терміново'),
        (CALLENGINEER, 'Невідомо, потрібен технічний інженер'),
        (UNKNOW, 'невідомо'),
        (NORMAL, 'В нормальному стані'),
    ]
    status = models.CharField(
        max_length=1,
        choices=MACHINE_STATUS,
        default=NORMAL,
    )


    NORMAL_CONDITION = '0'
    SMALLFAULT_RUNNING = '1'
    FAULT_SENDTECHORENG = '2'
    FAULT_CHECKEDTECHNICIAN = '3'
    FAULT_CHECKENGINEER = '4'
    FAULT = '5'
    UNDERREPAIR = '6'
    UNDERREPAIR_CALLENGINEER  = '7'
    
    MACHINE_CONDITION = [
        (NORMAL_CONDITION, 'В робочому стані'),
        (SMALLFAULT_RUNNING, 'Є не термінова несправність. Поки працює за графіком'),
        (FAULT_CHECKEDTECHNICIAN, 'Є несправність. Інформація переправлена техніку та інженеру'),
        (FAULT_SENDTECHORENG, 'Є несправність. Перевіряється техніком'),
        (FAULT_CHECKENGINEER, 'Є несправність. Інформацію дізнатись у інженера'),
        (FAULT, 'Є несправність'),
        (UNDERREPAIR, 'Знаходиться на ремонті'),
        (UNDERREPAIR_CALLENGINEER, 'На ремонті. Інформація у інженера'),
        
    ]

    machine_condition = models.CharField(
        max_length=1,
        choices=MACHINE_CONDITION,
        default=NORMAL_CONDITION,
    )


    brigade = models.ForeignKey(SeniorDriver, on_delete=models.CASCADE)

    work_days = models.IntegerField(default=0)
    last_used_data = models.DateField(default=datetime.date(2009, 10, 5))


    def lining_pidpiiki_list(self):

        pidpiiki = self.pidpiikies.values_list('empty', 'marka', 'count')
        mylist = []
        if not pidpiiki[0][0]:
            for item in pidpiiki:
                mylist.append(f"{item[1]} [{item[2]} шт.]")
        return mylist


    def lining_blocks_list(self):

        blocks = self.blocks.values_list('empty', 'marka', 'count')
        mylist = []
        if not blocks[0][0]:
            for item in blocks:
                string = f"{item[1]}" 
                string += f" [{item[2]} шт.]" if item[2] else ''
                mylist.append(string)
        return mylist


    def turbocharger_list(self):

        turbocharger = self.turbochargers.values_list('empty', 'marka')
        mylist = []
        if not turbocharger[0][0]:
            for item in turbocharger:
                mylist.append(f"{item[1]}")
        return mylist
    

    def compressor_list(self):

        compressor = self.compressors.values_list('empty', 'marka')
        mylist = []
        if not compressor[0][0]:
            for item in compressor:
                mylist.append(f"{item[1]}")
        return mylist


    def engine_list(self):

        engine = self.engines.values_list('empty', 'marka', 'number')
        mylist = []
        if not engine[0][0]:
            for item in engine:
                string = f"{item[1]}" 
                string += f" #{item[2]}" if item[2] else ''
                mylist.append(string)
        return mylist


    def battery_list(self):

        battery = self.batteries.values_list('empty', 'marka', 'count', 'last_replacement')
        mylist = []
        if not battery[0][0]:
            for item in battery:
                string = f"{item[1]}" 
                string += f" [{item[2]} шт.]" if item[2] else ''
                string += f". Дата заміни: {item[3]}" if item[3] else ''
                mylist.append(string)
        return mylist


    def transmission_fluid_list(self):
       
        transmission = self.transmission_fluid.values_list('empty', 'marka', 'volume')
        mylist = []
        if not transmission[0][0]:
            for item in transmission:
                string = f"{item[1]}" 
                string += f" [{item[2]} л.]" if item[2] else ''
                mylist.append(string)
        return mylist
    

    def hydraulic_fluid_list(self):

        hydraulic = self.hydraulic_fluid.values_list('empty', 'marka', 'volume') 
        mylist = []
        if not hydraulic[0][0]:
            for item in hydraulic:
                string = f"{item[1]}" 
                string += f" [{item[2]} л.]" if item[2] else ''
                mylist.append(string)
        return mylist


    def filter_list(self):
        
        filters = self.filters.values_list('empty', 'air', 'fuel', 'dizmaslo', 'gidravlichni') 
        mylist = []
        if not filters[0][0]:
            for item in filters:
                mylist.append(f"Air: {item[1]}, fuel: {item[2]}, dizmaslo: {item[3]}, gidravlichni: {item[4]}")
        return mylist


    def dizmaslo_list(self):

        dizmaslo = self.dizmaslos.values_list('empty', 'marka', 'volume')
        mylist = []
        if not dizmaslo[0][0]:
            for item in dizmaslo:
                mylist.append(f"{item[1]} [{item[2]} л.]")
        return mylist
    

    def full_name(self):
        return f"{self.machine.name} №{self.number_machine} [IN {self.inventory_number}]" 
    
    def short_name(self):
        return f"{self.machine.name} №{self.number_machine}" 


    def years_comission(self):
        from datetime import date
        diff = date.today() - self.year_of_commissioning
        return int(diff.days / 365)


    def __str__(self):
        return f"{self.machine.name} № {self.number_machine} [{self.inventory_number}]"


# ОПИСАНИЕ МАШИНЫ
class MachineName(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    image = models.ImageField(blank=True, upload_to="machines")
    
    def __str__(self):
        return f"{self.name}"


# СОСТОВЛЯЮЩИЕ МАШИНЫ
class Engine(models.Model):
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='engines')

    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=30, blank=True, null=True)
    number = models.CharField(max_length=30, blank=True, null=True)

    def info(self):
        return f"{self.marka} #{self.number}"

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            string += f" №{self.number}" if self.number else ''
            return string


class Turbocharger(models.Model):
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='turbochargers')

    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            return string




class LiningPidpiiki(models.Model):
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='pidpiikies')

    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=30, blank=True, null=True)
    count = models.CharField(max_length=10, blank=True, null=True)

    def info(self):
        return f"{self.marka} [{self.count} шт.]"

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            string += f"[{self.count} шт.]" if self.count else ''
            return string

class LiningBlock(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='blocks')
    
    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=30, blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            string += f"[{self.count} шт.]" if self.count else ''
            return string

class Compressor(models.Model):
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='compressors')
    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            return string

class Battery(models.Model):

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='batteries')
    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=40, blank=True, null=True)
    count = models.CharField(max_length=30, blank=True, null=True)
    last_replacement = models.DateField(blank=True, null=True)


    def info(self):
        return f"{self.marka} [{self.count} шт.]"

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            string += f"[{self.count} шт.]" if self.count else ''
            string += f". Ост. заміна {self.last_replacement}" if self.last_replacement else ''
            return string



class Dizmaslo(models.Model):
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='dizmaslos')

    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=50, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            string += f"[{self.volume} л.]" if self.volume else ''
            return string

class TransmissionFluid(models.Model):
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='transmission_fluid')

    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=50, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            string += f"[{self.volume} л.]" if self.volume else ''
            return string
    


class HydraulicFluid(models.Model):
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='hydraulic_fluid')

    empty = models.BooleanField(default=False)
    marka = models.CharField(max_length=50, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"{self.marka}" if self.marka else ''
            string += f"[{self.volume} л.]" if self.volume else ''
            return string

class Filter(models.Model):

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='filters')

    empty = models.BooleanField(default=False)
    air = models.CharField(max_length=50, blank=True, null=True)
    fuel = models.CharField(max_length=50, blank = True, null=True)
    dizmaslo = models.CharField(max_length=50, blank=True, null=True)
    gidravlichni = models.CharField(max_length=50, blank = True, null=True)

    def __str__(self):
        if self.empty:
            return "Дані відсутні"
        else:
            string = ''
            string += f"air: {self.air}; " if self.air else ''
            string += f"fuel: {self.fuel}; " if self.fuel else ''
            string += f"dizmaslo: {self.dizmaslo}; " if self.dizmaslo else ''
            string += f"gidrav: {self.gidravlichni}; " if self.gidravlichni else ''
            return string