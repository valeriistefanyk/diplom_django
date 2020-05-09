from django.core.management.base import BaseCommand

from main.management.commands.init_users_perm_db import Command as UserCommand
from main.management.commands.init_machines_db import Command as MachineCommand
from main.management.commands.init_reports_db import Command as ReportCommand
from main.management.commands.create_csv_machinist import Command as MachinistCommand


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        UserCommand().handle()
        MachineCommand().handle()
        ReportCommand().handle()
        MachinistCommand().handle()

        