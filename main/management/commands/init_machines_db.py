from django.core.management.base import BaseCommand
from machines.models import Machine, MachineName, Battery, Compressor, Dizmaslo, Engine, Filter, HydraulicFluid, LiningBlock, LiningPidpiiki, TransmissionFluid, Turbocharger
from django.contrib.auth.models import User


class Command(BaseCommand):

    def test_data(self):
        print('transmissionFluids: ', read_csv(filename='transmissionFluids'))
        print()
        print('turbochargers: ', read_csv(filename='turbochargers'))
        print()
        # print(read_csv(filename='hydraulicFluids'))
        # print(read_csv(filename='liningBlocks'))
        # print(read_csv(filename='liningPidpiikis'))

        # for element in data_machine_names:
        #     print(f'id: {element["id"]}, {element["inventory_number"]}')
        

    def init_machine_names(self):

        data_machine_names = read_csv()
        for element in data_machine_names:
            MachineName.objects.create(id=element["id"], name=element["name"], description=element["description"], image=element["image"])
        print("Дані в таблиці MachineName створені")
        

    def init_machines(self):

        data_machines = read_csv(filename='machines')
        machinenames = MachineName.objects.all()
        for element in data_machines:
            
            machine = Machine.objects.create(
                id=element["id"], 
                machine_id=element["machine_id"],
                name= machinenames.get(pk=element["machine_id"]).name,
                inventory_number=element["inventory_number"],
                number_machine=element["number_machine"],
                brigade_id=element["brigade_id"],
            )

            if element["year_of_commissioning"]:
                machine.year_of_commissioning= element["year_of_commissioning"]
            if element["initial_value"]:
                machine.initial_value= element["initial_value"]
            if element["residual_value"]:
                machine.residual_value= element["residual_value"]
            if element["depreciation_end_date"]:
                machine.depreciation_end_date= element["depreciation_end_date"]
            if element["rated_capacity"]:
                machine.rated_capacity= element["rated_capacity"]
            if element["diametr_wheel_pairs"]:
                machine.diametr_wheel_pairs= element["diametr_wheel_pairs"]
            if element["dizmaslo"]:
                machine.dizmaslo= element["dizmaslo"]
            if element["costs_at_rate"]:
                machine.costs_at_rate= element["costs_at_rate"]
            if element["date_ost_kr"]:
                machine.date_ost_kr= element["date_ost_kr"]
            if element["breakage_date"]:
                machine.breakage_date= element["breakage_date"]

            machine.save()

        print("Дані в таблиці Machine створені")


    def init_batteries(self):
        data_batteries = read_csv(filename='batteries')
        for element in data_batteries:
            battery = Battery.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            if element["marka"]:
                battery.marka = element["marka"]
            if element["count"]:
                battery.count = element["count"]
            if element["last_replacement"]:
                battery.last_replacement = element["last_replacement"]
            battery.save() 
        print("Дані в таблиці Battery створені")


    def init_compressors(self):
        data_compressors = read_csv(filename='compressors')
        for element in data_compressors:
            compressor = Compressor.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            if element["marka"]:
                compressor.marka = element["marka"]
            compressor.save() 
        print("Дані в таблиці Compressor створені")
    

    def init_dizmaslos(self):
        data_dizmaslos = read_csv(filename='dizmaslos')
        for element in data_dizmaslos:
            dizmaslo = Dizmaslo.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            if element["marka"]:
                dizmaslo.marka = element["marka"]
            if element["volume"]:
                dizmaslo.volume = element["volume"]
            dizmaslo.save() 
        print("Дані в таблиці Dizmaslo створені")
    

    def init_engines(self):
        data_engines = read_csv(filename='engines')
        for element in data_engines:
            engine = Engine.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            if element["marka"]:
                engine.marka = element["marka"]
            if element["number"]:
                engine.number = element["number"]
            engine.save() 
        print("Дані в таблиці Engine створені")
    

    def init_filters(self):
        data_filters = read_csv(filename='filters')
        for element in data_filters:
            filter_m = Filter.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            
            if element["air"]:
                filter_m.air = element["air"]
            if element["fuel"]:
                filter_m.fuel = element["fuel"]
            if element["dizmaslo"]:
                filter_m.dizmaslo = element["dizmaslo"]
            if element["gidravlichni"]:
                filter_m.gidravlichni = element["gidravlichni"]
            filter_m.save() 
        print("Дані в таблиці Filter створені")


    def init_hydraulicFluids(self):
        data_hydraulicFluids = read_csv(filename='hydraulicFluids')
        for element in data_hydraulicFluids:
            hydraulicFluid = HydraulicFluid.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            
            if element["marka"]:
                hydraulicFluid.marka = element["marka"]
            if element["volume"]:
                hydraulicFluid.volume = element["volume"]
            hydraulicFluid.save() 
        print("Дані в таблиці HydraulicFluid створені")
    

    def init_liningBlocks(self):
        data_liningBlocks = read_csv(filename='liningBlocks')
        for element in data_liningBlocks:
            liningBlock = LiningBlock.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            
            if element["marka"]:
                liningBlock.marka = element["marka"]
            if element["count"]:
                liningBlock.count = element["count"]
            liningBlock.save() 
        print("Дані в таблиці LiningBlock створені")
    

    def init_liningPidpiikis(self):
        data_liningPidpiikis = read_csv(filename='liningPidpiikis')
        for element in data_liningPidpiikis:
            liningPidpiiki = LiningPidpiiki.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            
            if element["marka"]:
                liningPidpiiki.marka = element["marka"]
            if element["count"]:
                liningPidpiiki.count = element["count"]
            liningPidpiiki.save() 
        print("Дані в таблиці LiningPidpiiki створені")


    def init_transmissionFluids(self):
        data_transmissionFluids = read_csv(filename='transmissionFluids')
        for element in data_transmissionFluids:
            transmissionFluid = TransmissionFluid.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            
            if element["marka"]:
                transmissionFluid.marka = element["marka"]
            if element["volume"]:
                transmissionFluid.volume = element["volume"]
            transmissionFluid.save() 
        print("Дані в таблиці TransmissionFluid створені")
    

    def init_turbochargers(self):
        data_turbochargers = read_csv(filename='turbochargers')
        for element in data_turbochargers:
            turbocharger = Turbocharger.objects.create(id=element["id"], machine_id=element["machine_id"], empty=element["empty"])
            
            if element["marka"]:
                turbocharger.marka = element["marka"]
            turbocharger.save() 
        print("Дані в таблиці Turbocharger створені")



    def init(self):
        if not User.objects.all():
            print('Помилка ініціалізації. Спочатку виконайте команду "python manage.py init_users_perm_db"')
            return
        self.init_machine_names()
        self.init_machines()
        self.init_batteries()
        self.init_compressors()
        self.init_dizmaslos()
        self.init_engines()
        self.init_filters()
        self.init_hydraulicFluids()
        self.init_liningBlocks()
        self.init_liningPidpiikis()
        self.init_transmissionFluids()
        self.init_turbochargers()
        # self.test_data()


    def handle(self, *args, **kwargs):
        print("\nІніціалізація даних колійних машин...\n")
        self.init()
        print("\nІніціалізація завершена\n")


### Допоміжні методи ###
def read_data_csv(filename='machines_name'):
    import csv
    location = f"files/static/other_data/machine_tables/{filename}.csv"
    with open(location, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n', quotechar=',')
        row_array = []
        for row in spamreader:
            row_array.append(row)

    return row_array

def read_csv(filename = 'machines_name', db_tables = 'machine_tables'):
    import csv
    file_location = 'files/static/other_data/' + db_tables + '/' + filename + '.csv'
    with open(file_location, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        a = list(reader)
        return a