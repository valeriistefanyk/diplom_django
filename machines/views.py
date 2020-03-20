from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from machines import models


def all_machines(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    machiness = models.Machine.objects.all()
    
    query = request.GET.get('q')
    if query:
        machiness = machiness.filter(
            Q(machine__name__icontains=query) | Q(inventory_number__icontains=query) |
            Q(number_machine__icontains=query)
        ).distinct()
    
    paginator = Paginator(machiness, 10)
    page = request.GET.get('page')
    try:
        machines = paginator.page(page)
    except EmptyPage:
        machines = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        machines = paginator.page(1)

    context = {
        'machines': machines
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


def show_machines_description(request):
    
    machines = models.MachineName.objects.all()
    context = {
        'machines': machines
    }
    return render(request, 'machines/machines_description.html', context)
