from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Engineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=False)
    
    def __str__(self):
        return f"{self.user.username}"