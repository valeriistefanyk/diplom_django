from django.core.management.base import BaseCommand
from machines.models import Machine
from senior_driver.models import SeniorDriver
from engineer.models import Report, MachineReport
import datetime
import random


class Command(BaseCommand):
    
    def init_data(self, days = 30, machines_count_checkded = 3, machines_count_unchecked = 2): 
        
        date_list = []

        for i in range(days, 0, -1):
            date_list.append(datetime.date.today()-datetime.timedelta(days=i))

        drivers = SeniorDriver.objects.all()
        if not drivers:
            print('Помилка ініціалізації. Спочатку виконайте команду "python manage.py init_users_perm_db"')
            return
        
        machines = Machine.objects.all()
        if not machines:
            print('Помилка ініціалізації. Спочатку виконайте команду "python manage.py init_machines_db"')
            return

        for i in range(0, len(date_list)-1):
            for driver in drivers:
                report = Report.objects.create(
                    filled_up = driver,
                    date = date_list[i],
                    checked = True,
                )

                concrete_machines = machines.filter(brigade=driver)[:machines_count_checkded] 
                for machine in concrete_machines:
                    machine_report = MachineReport.objects.create(
                        report = report,
                        machine = machine,
                        name = machine.short_name(),
                        motohour = random.randint(5, 70),
                        fuel = round(random.uniform(20, 60), 1),
                        breakage = False
                    )
                    machine.last_used_data = date_list[i]
                    machine.save()
                    

        for i in range(len(date_list)-1, len(date_list)):
            for driver in drivers:
                report = Report.objects.create(
                    filled_up = driver,
                    date = date_list[i],
                    checked = False,
                )

                concrete_machines = machines.filter(brigade=driver)[:machines_count_unchecked] 
                for machine in concrete_machines:
                    MachineReport.objects.create(
                        report = report,
                        machine = machine,
                        name = machine.short_name(),
                        motohour = random.randint(5, 70),
                        fuel = round(random.uniform(20, 60), 1),
                        breakage = False
                    )
                    machine.last_used_data = date_list[i]
                    machine.save()


    def handle(self, *args, **kwargs):
        print("\nІніціалізація даних звітів...")
        self.init_data(7, 3, 3)
        print("Ініціалізація завершена\n")
        