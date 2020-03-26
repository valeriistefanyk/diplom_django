from django.contrib import admin
from engineer import models


# Register your models here.
class ReportInline(admin.TabularInline):
    model = models.MahineReport
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    inlines = [
        ReportInline,
    ]

admin.site.register(models.Engineer)