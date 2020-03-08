from django.shortcuts import render

from machines import models

def all_machines(request):
    machines = models.Machine.objects.all()
    latest_machines_list = machines[:5]
    context = {
        'latest_machines': latest_machines_list
    }
    return render(request, 'machines/machines.html', context=context)

def detail_machine(request):

    return render(request, 'machines/detail_machine.html')