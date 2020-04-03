from django.core.management.base import BaseCommand
from machines.models import Machine
from senior_driver.models import SeniorDriver
from engineer.models import Report, MachineReport
import datetime
import random


class Command(BaseCommand):
    
    def init_data(self): 
        
        reports = Report.objects.all()
        reports.delete()

        


        


    def handle(self, *args, **kwargs):
        print("Delete all report data")
        self.init_data()