from django.core.management.base import BaseCommand
from machines.models import Machine, MachineName
from machines import models as modelsMachine
from senior_driver.models import SeniorDriver
from engineer.models import Report, MachineReport, Engineer
from director.models import Director
from senior_driver.models import SeniorDriver
from django.contrib.auth.models import User
import datetime
import random
import csv


class Command(BaseCommand):
    
    def create_csv(self, objects, filename, db_tables = 'machine_tables'):
        objects = list(objects)
        keys = objects[0].keys()
        
        file_location = 'files/static/other_data/' + db_tables + '/' + filename + '.csv'
        
        with open(file_location, 'w', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(objects)
        return objects

    def read_csv(self, filename, db_tables = 'machine_tables'):

        file_location = 'files/static/other_data/' + db_tables + '/' + filename + '.csv'
        with open(file_location, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            a = list(reader)
            return a


    def create_machine_csv(self):

        machines = Machine.objects.values('id','machine_id', 'inventory_number', 'number_machine', 'year_of_commissioning', 'rated_capacity', 
                                'costs_at_rate', 'dizmaslo', 'diametr_wheel_pairs', 'date_ost_kr', 'initial_value', 'residual_value', 
                                'depreciation_end_date', 'breakage', 'breakage_date', 'breakage_info', 'brigade_id')
        machinenames = MachineName.objects.values('id', 'name', 'description', 'image')
        engines = modelsMachine.Engine.objects.values('id', 'machine_id', 'empty', 'marka', 'number')
        turbochargers = modelsMachine.Turbocharger.objects.values('id', 'machine_id', 'empty', 'marka')
        liningPidpiikis = modelsMachine.LiningPidpiiki.objects.values('id', 'machine_id', 'empty', 'marka', 'count')
        liningBlocks = modelsMachine.LiningBlock.objects.values('id', 'machine_id', 'empty', 'marka', 'count')
        compressors = modelsMachine.Compressor.objects.values('id', 'machine_id', 'empty', 'marka')
        batteries = modelsMachine.Battery.objects.values('id', 'machine_id', 'empty', 'marka', 'count', 'last_replacement')
        dizmaslos = modelsMachine.Dizmaslo.objects.values('id', 'machine_id', 'empty', 'marka', 'volume')
        transmissionFluids = modelsMachine.TransmissionFluid.objects.values('id', 'machine_id', 'empty', 'marka', 'volume')
        hydraulicFluids = modelsMachine.HydraulicFluid.objects.values('id', 'machine_id', 'empty', 'marka', 'volume')
        filters = modelsMachine.Filter.objects.values('id', 'machine_id', 'empty', 'air', 'fuel', 'dizmaslo', 'gidravlichni')

        objects_list = [(machines, 'machines'), 
                        (machinenames, 'machines_name'),
                        (engines, 'engines'),
                        (turbochargers, 'turbochargers'),
                        (liningPidpiikis, 'liningPidpiikis'),
                        (liningBlocks, 'liningBlocks'),
                        (compressors, 'compressors'),
                        (batteries, 'batteries'),
                        (dizmaslos, 'dizmaslos'),
                        (transmissionFluids, 'transmissionFluids'),
                        (hydraulicFluids, 'hydraulicFluids'),
                        (filters, 'filters'),
            ]
        for object_list in objects_list:
            self.create_csv(object_list[0], object_list[1], db_tables='machine_tables')
    

    def read_machine_csv(self):
        
        filenames = ['machines', 'machines_name', 'engines', 'turbochargers', 'liningPidpiikis', 'liningBlocks', 
                    'compressors', 'batteries', 'dizmaslos', 'transmissionFluids', 'hydraulicFluids', 'filters']
        for filename in filenames:
            print(f'{filename}: {self.read_csv(filename, db_tables="machine_tables")}\n\n')


    def create_users_csv(self):
        
        users = User.objects.values('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

        engineers = Engineer.objects.values('id', 'user_id', 'date_of_birth', 'telephone1', 'telephone2', 'avatar')
        directors = Director.objects.values('id', 'user_id', 'date_of_birth', 'telephone1', 'telephone2', 'avatar')
        drivers = SeniorDriver.objects.values('id', 'user_id', 'brigade_name', 'date_of_birth', 'telephone1', 'telephone2', 'avatar')
    
        objects_list = [(users, 'users'), 
                        (directors, 'directors'), 
                        (engineers, 'engineers'), 
                        (drivers, 'drivers')
            ]
        for object_list in objects_list:
            self.create_csv(object_list[0], object_list[1], db_tables='user_tables')
    

    def read_users_csv(self):
        
        filenames = ['users', 'engineers', 'drivers', 'directors']
        for filename in filenames:
            print(f'{filename}: {self.read_csv(filename, db_tables="user_tables")}\n\n')


    def create_reports_csv(self):
        
        reports = Report.objects.values('id', 'filled_up_id', 'date_of_completion', 'updated_data', 'date', 'checked')
        machinereports = MachineReport.objects.values('id', 'report_id', 'machine_id', 'motohour', 'fuel', 'breakage')
        
        objects_list = [(reports, 'reports'), (machinereports, 'machinereports')]
        
        for object_list in objects_list:
            self.create_csv(object_list[0], object_list[1], db_tables='report_tables')
    

    def read_reports_csv(self):
        
        filenames = ['reports', 'machinereports']
        for filename in filenames:
            print(f'{filename}: {self.read_csv(filename, db_tables="report_tables")}\n\n')


    # main file
    def handle(self, *args, **kwargs):
        print("Create csv file")
        
        self.read_reports_csv()