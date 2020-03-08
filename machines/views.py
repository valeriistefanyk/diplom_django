from django.shortcuts import render
from django.shortcuts import get_object_or_404

from machines import models

def all_machines(request):
    machines = models.Machine.objects.all()
    latest_machines_list = machines[:5]
    context = {
        'latest_machines': latest_machines_list
    }
    return render(request, 'machines/machines.html', context=context)

def detail_machine(request, id):
    machine = get_object_or_404(models.Machine, pk=id)
    
    context = {
        'machine': machine,
    }
    
    return render(request, 'machines/detail_machine.html', context)