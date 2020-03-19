from django.shortcuts import render, redirect
from django.http import Http404

from engineer import models
from machines.models import Machine
import datetime


# Стартова сторінка інженера
def hello_page(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    return render(request, 'engineer/home_page.html')


# Відображення звітів
def showReports(request):
    """Відображення звіту для інженера"""
    
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    if request.method == "POST":
        checked = request.POST.get('checked')
        report_id = request.POST.get('report_id')
        
        if checked == "True":
            report = models.Report.objects.get(pk=report_id)
            report.checked = True
            report.save()

    reports = models.Report.objects.all()

    context = {
        'reports': reports,
        'reports_forwarded': reports.filter(checked=True),
        'reports_unforwarded': reports.filter(checked=False),
    }
    return render(request, 'engineer/show_reports.html', context)


# Старші водії
def show_drivers(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

    from senior_driver.models import SeniorDriver

    drivers = SeniorDriver.objects.all()
    context = {
        'drivers': drivers
    }
    return render(request, 'engineer/show_drivers.html', context)


# Графік роботи / звітність 
def work_days(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

    context = {}
    return render(request, 'engineer/work_days.html', context)


# Машини які перебувають/перебували у ремонті
def show_fix_machines(request):
    
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

    if request.method == "POST":
        breakage = request.POST.get('breakage')
        machine_id = request.POST.get('breakage_machine')
        
        if breakage == "False":
            machine = models.Machine.objects.get(pk=machine_id)
            machine.breakage = False
            machine.breakage_info = f"{machine.breakage_info}\nUPDATE: Машина була починена {datetime.date.today()}"
            machine.save()

    breakage_machines = Machine.objects.filter(breakage=True).order_by('-brigade')
    context = {
        'breakage_machines': breakage_machines
    }
    return render(request, 'engineer/fix_machines.html', context)