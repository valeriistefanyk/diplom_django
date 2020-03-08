from django.db import models
from django.contrib.auth.models import User

from senior_driver.models import SeniorDriver
from machines.models import Machine


# Create your models here.

class Engineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=False)
    
    def __str__(self):
        return f"{self.user.username}"


class Report(models.Model):
    
    filled_up = models.ForeignKey(SeniorDriver, on_delete=models.CASCADE)
    date_of_completion = models.DateTimeField(auto_now=True)
    date = models.DateField()

    motohour = models.FloatField()
    fuel = models.FloatField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    breakage = models.BooleanField(default=False)

    checked = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"{self.filled_up} - {self.date}"
