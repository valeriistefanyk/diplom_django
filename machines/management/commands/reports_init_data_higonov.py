from django.core.management.base import BaseCommand
from machines.models import Machine
from senior_driver.models import SeniorDriver
from engineer.models import Report
import datetime
import random


class Command(BaseCommand):
    
    def init_data(self): 
        
        date_list = []

        for i in range(30, 0, -1):
            date_list.append(datetime.date.today()-datetime.timedelta(days=i))

        driver = SeniorDriver.objects.filter(user__username='higonov')[0]
        machines = Machine.objects.filter(brigade=driver)
        machine1 = machines[1]
        machine10 = machines[10]


        for i in range(0, len(date_list)):
            Report.objects.create(
                filled_up = driver,
                date = date_list[i],
                motohour = random.randint(5, 70),
                fuel = round(random.uniform(20, 60), 1),
                machine = machine1,
                checked = True,
            )
            Report.objects.create(
                filled_up = driver,
                date = date_list[i],
                motohour = random.randint(5, 70),
                fuel = round(random.uniform(20, 60), 1),
                machine = machine10,
                checked = True,
            )


        


    def handle(self, *args, **kwargs):
        print("Initializes data for machine model")
        self.init_data()