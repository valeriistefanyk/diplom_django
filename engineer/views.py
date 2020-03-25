from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from engineer import models
from machines.models import Machine
from senior_driver.models import SeniorDriver
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
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if from_date and to_date:
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)
        reports = reports.filter(date__range = [from_date_correct, to_date_correct])
        print(reports)

    context = {
        'from_date': from_date,
        'to_date' : to_date,
        'reports': reports,
        'reports_forwarded': reports.filter(checked=True).order_by('date'),
        'reports_unforwarded': reports.filter(checked=False).order_by('date'),
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

    drivers = SeniorDriver.objects.all().order_by('brigade_name')
    context = {
        'drivers': drivers
    }
    return render(request, 'engineer/show_drivers.html', context)


# Деталбна інформація про водія
def show_drivers_detail(request, username):
    
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

    driver = get_object_or_404(SeniorDriver, user__username=username)
    reports_driver = models.Report.objects.filter(filled_up=driver)

    context = {
        'driver': driver,
        'reports_driver': reports_driver, 
    }
    return render(request, 'engineer/show_driver_detail.html', context)


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


# ПРАВИЛЬНА ДАТА
def correct_date(date):
    date_list = date.split('/')
    date_correct = f"{date_list[2]}-{date_list[0]}-{date_list[1]}"
    return date_correct