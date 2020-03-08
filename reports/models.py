from django.db import models
from senior_driver.models import SeniorDriver
from machines.models import Machine

# Create your models here.
class Report(models.Model):
    filled_up = models.ForeignKey(SeniorDriver, on_delete=models.CASCADE)
    date_of_completion = models.DateTimeField(auto_now=True)
    date = models.DateField()

    motohour = models.FloatField()
    fuel = models.FloatField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.filled_up} - {self.date}"
