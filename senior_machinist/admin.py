from django.contrib import admin
from senior_machinist.models import SeniorMachinist, BrigadeMembers, BrigadeInfoReport, MasloInfoReport, MotoAndFuelInfoReport, TempReport, MachineWorkingReport


admin.site.register(SeniorMachinist)
admin.site.register(BrigadeMembers)
admin.site.register(BrigadeInfoReport)
admin.site.register(MasloInfoReport)
admin.site.register(MotoAndFuelInfoReport)
admin.site.register(TempReport)
admin.site.register(MachineWorkingReport)