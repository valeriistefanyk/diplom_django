def read_data_xls(*argv):
    import xlrd
    import datetime
    loc = ("static_files/other_data/machines_bd.xls") 
  
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    
    row_array = []
    for i in range(5, sheet.nrows - 1):
        row_array.append(sheet.row_values(i))
    for i in range(len(row_array)):
        for j in (3, 26, 29):
            if isinstance(row_array[i][j], float):
                row_array[i][j] = datetime.datetime(*xlrd.xldate_as_tuple(row_array[i][j], wb.datemode)) 
    for i in row_array:
        i.pop()

    return row_array


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