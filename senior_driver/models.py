from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SeniorDriver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=False)
    brigade_name = models.CharField(blank=True, max_length=50)
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