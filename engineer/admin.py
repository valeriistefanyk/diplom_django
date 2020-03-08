from django.contrib import admin
from engineer import models

# Register your models here.
admin.site.register(models.Engineer)
admin.site.register(models.Report)