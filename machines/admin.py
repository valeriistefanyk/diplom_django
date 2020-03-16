from django.contrib import admin
from machines import models


# Register your models here.
admin.site.register(models.Machine)
admin.site.register(models.MachineName)