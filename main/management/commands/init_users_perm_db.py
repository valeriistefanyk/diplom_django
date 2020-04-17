from django.core.management.base import BaseCommand
from machines.models import Machine, MachineName
from director.models import Director
from engineer.models import Engineer
from senior_driver.models import SeniorDriver
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from faker import Faker


CONTENT_TYPE = {
    'driver': ContentType.objects.get_for_model(SeniorDriver),
    'director': ContentType.objects.get_for_model(Director),
    'engineer': ContentType.objects.get_for_model(Engineer)
}


class Command(BaseCommand):
    
    def test_data(self):
        fake = Faker('uk_UA')
        users = read_csv(filename='drivers')
        print(f'{users}')
    
    def create_permissions(self):
        """ Створення дозволів """

        Permission.objects.create(codename='full_control', name = 'SeniorDriver full control', content_type=CONTENT_TYPE['driver'])
        Permission.objects.create(codename='full_control', name = 'Engineer full control', content_type=CONTENT_TYPE['engineer'])
        Permission.objects.create(codename='full_control', name = 'Director full control', content_type=CONTENT_TYPE['director'])
        
        Permission.objects.create(codename='part_control', name = 'SeniorDriver part control', content_type=CONTENT_TYPE['driver'])
        Permission.objects.create(codename='part_control', name = 'Engineer part control', content_type=CONTENT_TYPE['engineer'])
        Permission.objects.create(codename='part_control', name = 'Director part control', content_type=CONTENT_TYPE['director'])

        print("Дані в таблиці Permission створені")


    def init_users(self):
        fake = Faker('uk_UA')
        users = read_csv(filename='users')
        for user in users:
            if not user["username"]:
                continue
            if user["username"] == 'admin':
                User.objects.create_superuser(
                    id=user["id"],
                    username=user["username"],
                    password='admin',
                    email=user["email"],
                    first_name='Admin',
                    last_name='Adminov',
                )
                continue
            
            User.objects.create_user(
                id=user["id"],
                username=user["username"],
                password='123456',  
                email=user["email"],
                first_name=user["first_name"] if user["first_name"] else (fake.name()).split(' ')[-2],
                last_name=user["last_name"] if user["last_name"] else (fake.name()).split(' ')[-1],
            )
        print("Дані в таблиці User створені")


    def init_directors(self):
        directors = read_csv(filename='directors')
        for director in directors:
            Director.objects.create(
                id=director["id"], 
                user_id=director["user_id"], 
                telephone1=director["telephone1"], 
                telephone2=director["telephone2"], 
                date_of_birth=director["date_of_birth"],
                avatar=director["avatar"])

            user = User.objects.get(pk=director["user_id"])
            addPermission(user, 'full_control', 'director')
            addPermission(user, 'part_control', 'director')
        print("Дані в таблиці Director створені")


    def init_engineers(self):
        engineers = read_csv(filename='engineers')
        for engineer in engineers:
            obj = Engineer.objects.create(
                id=engineer["id"], 
                user_id=engineer["user_id"], 
                date_of_birth=engineer["date_of_birth"],
                avatar=engineer["avatar"])

            check_telephones(obj, engineer["telephone1"], engineer["telephone2"])
            
            user = User.objects.get(pk=engineer["user_id"])
            addPermission(user, 'full_control', 'engineer')
            addPermission(user, 'part_control', 'engineer')
        print("Дані в таблиці Engineer створені")

    def init_drivers(self):
        drivers = read_csv(filename='drivers')
        for driver in drivers:
            obj = SeniorDriver.objects.create(
                id=driver["id"], 
                user_id=driver["user_id"], 
                date_of_birth=driver["date_of_birth"],
                brigade_name=driver["brigade_name"],
                avatar=driver["avatar"])

            check_telephones(obj, driver["telephone1"], driver["telephone2"])
            
            user = User.objects.get(pk=driver["user_id"])
            addPermission(user, 'full_control', 'driver')
            addPermission(user, 'part_control', 'driver')
        print("Дані в таблиці Driver створені")

    def init(self):
        self.create_permissions()
        self.init_users()
        self.init_directors()
        self.init_engineers()
        self.init_drivers()

        # self.test_data()


    def handle(self, *args, **kwargs):
        print("\nІніціалізація даних користувачів...\n")
        self.init()
        print("\nІніціалізація завершена\n")



### Допоміжні методи ###

def read_csv(filename = 'users', db_tables = 'user_tables'):
    import csv
    file_location = 'files/static/other_data/' + db_tables + '/' + filename + '.csv'
    with open(file_location, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        a = list(reader)
        return a


def addPermission(user, codename, status):
    
    permission = Permission.objects.get(
                codename=codename,
                content_type=CONTENT_TYPE[status],
            )
    user.user_permissions.add(permission)


def check_telephones(obj, telephone1=None, telephone2=None):
    if telephone1:
        obj.telephone1 = telephone1
    if telephone2:
        obj.telephone2 = telephone2
    obj.save()