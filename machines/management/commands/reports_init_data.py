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

        for i in range(0, len(date_list)-1):
            for driver in drivers:
                report = Report.objects.create(
                    filled_up = driver,
                    date = date_list[i],
                    motohour = random.randint(5, 70),
                    fuel = round(random.uniform(20, 60), 1),
                    machine = Machine.objects.all()[0],
                    checked = True,
                )

                concrete_machines = Machine.objects.filter(brigade=driver)[:machines_count_checkded] 
                for machine in concrete_machines:
                    MachineReport.objects.create(
                        report = report,
                        machine = machine,
                        motohour = random.randint(5, 70),
                        fuel = round(random.uniform(20, 60), 1),
                        breakage = False
                    )

        for i in range(len(date_list)-1, len(date_list)):
            for driver in drivers:
                report = Report.objects.create(
                    filled_up = driver,
                    date = date_list[i],
                    motohour = random.randint(5, 70),
                    fuel = round(random.uniform(20, 60), 1),
                    machine = Machine.objects.all()[0],
                    checked = False,
                )

                concrete_machines = Machine.objects.filter(brigade=driver)[:machines_count_unchecked] 
                for machine in concrete_machines:
                    MachineReport.objects.create(
                        report = report,
                        machine = machine,
                        motohour = random.randint(5, 70),
                        fuel = round(random.uniform(20, 60), 1),
                        breakage = False
                    )


        


    def handle(self, *args, **kwargs):
        print("Initializes data for machine model")
        self.init_data(7, 3, 3)