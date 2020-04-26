from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from machines import models


@login_required
def all_machines(request):

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


@login_required
def detail_machine(request, id):

    machine = get_object_or_404(models.Machine, pk=id)
    context = {
        'machine': machine,
    }
    return render(request, 'machines/detail_machine.html', context)


@login_required
def show_detail_machines(request):

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
    return render(request, 'machines/detail_machines.html', context=context)



def show_machines_description(request):
    
    machines = models.MachineName.objects.all().prefetch_related('machine_set')
    context = {
        'machines': machines
    }
    return render(request, 'machines/machines_description.html', context)
