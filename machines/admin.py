from django.contrib import admin
from machines import models


# Register your models here.
class EngineInline(admin.TabularInline):
    model = models.Engine
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class TurbochargerInline(admin.TabularInline):
    model = models.Turbocharger
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class CompressorInline(admin.TabularInline):
    model = models.Compressor
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class LiningPidpiikiInline(admin.TabularInline):
    model = models.LiningPidpiiki
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class TransmissionFluidInline(admin.TabularInline):
    model = models.TransmissionFluid
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class HydraulicFluidInline(admin.TabularInline):
    model = models.HydraulicFluid
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class BatteryInline(admin.TabularInline):
    model = models.Battery
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class FilterInline(admin.TabularInline):
    model = models.Filter
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class DizmasloInline(admin.TabularInline):
    model = models.Dizmaslo
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class LiningBlockInline(admin.TabularInline):
    model = models.LiningBlock
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

@admin.register(models.Machine)
class MachineAdmin(admin.ModelAdmin):
    # fields = ('inventory_number', 'number_machine')
    inlines = [
        EngineInline,
        TurbochargerInline,
        FilterInline,
        LiningBlockInline,
        LiningPidpiikiInline,
        CompressorInline,
        BatteryInline,
        DizmasloInline,
        TransmissionFluidInline,
        HydraulicFluidInline,
    ]

admin.site.register(models.MachineName)