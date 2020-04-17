from django.db import models
from django.contrib.auth.models import User

from senior_driver.models import SeniorDriver
from machines.models import Machine


class Engineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=False)
    telephone1 = models.CharField(max_length=15, blank=True, default='')
    telephone2 = models.CharField(max_length=15, blank=True, default='')
    avatar = models.ImageField(blank=True, upload_to="employees")


    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def phones(self):
        phones = self.telephone1
        if self.telephone2:
            phones += ', ' + self.telephone2
        return phones

    def __str__(self):
        return f"{self.user.username}"


class Report(models.Model):
    """ Таблиця Report - звіти від старших водіїв """
    
    filled_up = models.ForeignKey(SeniorDriver, on_delete=models.CASCADE)
    date_of_completion = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)
    date = models.DateField()

    checked = models.BooleanField(blank=True, default=False)
    checked_by = models.ForeignKey(Engineer, on_delete=models.CASCADE, blank=True, null = True)

    def __str__(self):
        return f"{self.filled_up} - {self.date}"

class MachineReport(models.Model):
    """ Таблиця MachineReport - які машини були використані в ході робочого дня """
    
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    motohour = models.FloatField()
    fuel = models.FloatField()
    
    breakage = models.BooleanField(default=False)
    breakage_info = models.TextField(blank=True, null=True)
    breakage_date_start = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.report.date} - {self.machine}"
    