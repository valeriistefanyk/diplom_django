from django.core.management.base import BaseCommand
from machines.models import Machine, MachineName
from machines import models as modelsMachine
from senior_driver.models import SeniorDriver
from engineer.models import Report, MachineReport, Engineer
from director.models import Director
from senior_driver.models import SeniorDriver
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
import datetime
import random
import csv
from faker import Faker
from senior_machinist.models import SeniorMachinist, BrigadeMembers


CONTENT_TYPE = {
    'machinist': ContentType.objects.get_for_model(SeniorMachinist)
}


class Command(BaseCommand):
    
    def create_permissions(self):
        """ Створення дозволів """

        Permission.objects.create(codename='full_control', name = 'SeniorMachinist full control', content_type=CONTENT_TYPE['machinist'])
        Permission.objects.create(codename='part_control', name = 'SeniorMachinist part control', content_type=CONTENT_TYPE['machinist'])

    def create_csv(self, filename, db_tables = 'user_tables'):
        
        machinelist = Machine.objects.all()
        machinists = []
        fake = Faker('uk_UA')
        brigade_name = 0

        for machine in machinelist:
            name = fake.name_male()

            last_name = name.split(' ')[-1]
            first_name = name.split(' ')[-2]
            machine_id = machine.id
            brigade_name += 1
            telephone1 = fake.phone_number().replace(' ', '')
            telephone2 = fake.phone_number().replace(' ', '')
            email = fake.email()
            username = email.split('@')[0]
            password = '123456'
            date_start_work = generate_date('start_work')
            date_of_birth=generate_date('birthday')

            machinists.append({
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'telephone1': telephone1,
                'telephone2': telephone2,
                'email': email,
                'machine_id': machine_id,
                'brigade_name': brigade_name,
                'date_start_work': date_start_work,
                'date_of_birth': date_of_birth
            })

        file_location = 'files/static/other_data/' + db_tables + '/' + filename + '.csv'
        with open(file_location, "w", newline="", encoding='utf-8') as file:
            columns = ["username", "password", "first_name", "last_name", "telephone1", "telephone2", "email", "machine_id", "brigade_name", 'date_of_birth', "date_start_work"]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()

            writer.writerows(machinists)
            print(writer)
        print('created')

    def read_csv(self, filename, db_tables = 'user_tables'):

        file_location = 'files/static/other_data/' + db_tables + '/' + filename + '.csv'
        
        with open(file_location, "r", newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                user = User.objects.create_user(
                                    username=row['username'], 
                                    email=row['email'],
                                    password=row['password'],
                                    first_name=row['first_name'],
                                    last_name=row['last_name'],
                    )
                SeniorMachinist.objects.create(
                                    user = user,
                                    brigade_name = row["brigade_name"],
                                    telephone1 = row["telephone1"],
                                    telephone2 = row["telephone2"],
                                    machine_id = int(row["machine_id"]),
                                    date_of_birth = generate_date('birthday'),
                                    date_start_work = generate_date('start_work'),
                                    avatar = '/employees/no-image.png',
                    )
                addPermission(user, 'full_control', 'machinist')
                addPermission(user, 'part_control', 'machinist')
            print('Створено')
        
    def create_brigade_members(self):

        print("Створення членів бригади")
        machinists = SeniorMachinist.objects.all()
        fake = Faker('uk_UA')

        for machinist in machinists:
            for _ in range(6):
                name = fake.name_male()
                BrigadeMembers.objects.create(
                                    seniormachinist = machinist,
                                    first_name = name.split(' ')[-2],
                                    last_name = name.split(' ')[-1],
                                    telephone1 = fake.phone_number(),
                                    telephone2 = fake.phone_number(),
                    )
        print('Створення членів бригади завершенно')

    # main file
    def handle(self, *args, **kwargs):

        print("Створення машиністів")
        # self.create_permissions()
        # self.create_csv('machinists')
        # self.read_csv('machinists')
        self.create_brigade_members()



def generate_date(goal = 'birthday'):
    
    if goal == 'birthday':
        start_date = datetime.date(1980, 1, 1)
        end_date = datetime.date(1999, 2, 1)
    elif goal == 'start_work':
        start_date = datetime.date(2001, 1, 1)
        end_date = datetime.date.today()
    else:
        start_date = datetime.date(1980, 1, 1)
        end_date = datetime.date.today()

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


def addPermission(user, codename, status):
    
    permission = Permission.objects.get(
                codename=codename,
                content_type=CONTENT_TYPE[status],
            )
    user.user_permissions.add(permission)