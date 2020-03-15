from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Director(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=False)
    telephone1 = models.CharField(max_length=15, blank=True, default='')
    telephone2 = models.CharField(max_length=15, blank=True, default='')
    
    def __str__(self):
        return f"{self.user.username}"