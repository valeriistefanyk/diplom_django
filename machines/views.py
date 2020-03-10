from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from machines import models

def all_machines(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end


    machines = models.Machine.objects.all()
    latest_machines_list = machines[:5]
    context = {
        'latest_machines': latest_machines_list
    }
    return render(request, 'machines/machines.html', context=context)

def detail_machine(request, id):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end


    machine = get_object_or_404(models.Machine, pk=id)
    
    context = {
        'machine': machine,
    }
    
    return render(request, 'machines/detail_machine.html', context)