from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.db.models import Q, Sum
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from engineer import models
from machines.models import Machine
from senior_driver.models import SeniorDriver
from engineer.models import Engineer, MachineReport
import datetime


@login_required
@permission_required('engineer.full_control', raise_exception=True)
def hello_page(request):
    """ Стартова сторінка інженера """
    
    return render(request, 'engineer/home_page.html')


@login_required
@permission_required('engineer.full_control', raise_exception=True)
def show_unforwarded_reports(request):
    """Відображення невідправлених звітів """
    
    engineer = set_engineer(request.user)

    if request.method == "POST":
        report_id = request.POST.get('report_id')
        report = models.Report.objects.get(pk=report_id)
        report.checked = True
        report.checked_by = engineer
        report.save()
        

    reports_unforwarded = models.Report.objects.filter(checked=False).order_by('date')

    date_report_set = []
    reports_date = reports_unforwarded.values('date').annotate(total=Count('id'))
    for report_date in reports_date:
        date = report_date['date'].strftime("%Y-%m-%d")
        queryset_rep = reports_unforwarded.filter(date=date).select_related('filled_up', 'filled_up__user')
        reports_set = []
        for query in queryset_rep:
            report_id = query.id
            driver = query.filled_up.full_name()
            brigade_name = query.filled_up.brigade_name
            machines = []
            for machine in query.machinereport_set.values('name', 'fuel', 'motohour', 'breakage', 'breakage_info'):
                name = machine['name']
                fuel = machine['fuel']
                motohour = machine['motohour']
                
                breakage = "Є поломка" if machine['breakage'] else "Поломок не було"
                if breakage == "Є поломка":
                    if machine['breakage_info']:
                        breakage += f"<br>Інформація: {machine['breakage_info']}"
                    else:
                        breakage = f"<br>Інформація про поломку відсутня"
                        
                
                machines_info = {
                    'machine_short_name': name,
                    'machine_full_name': name,
                    'fuel': fuel,
                    'motohour': motohour,
                    'breakage': breakage,
                }

                machines.append(machines_info)

            reports_set.append({'report_id': report_id, 'driver': driver, 'brigade_name': brigade_name, 'machines': machines})
        date_report_set.append({'date': date, 'report_info': reports_set})
    

    context = {
        'date_report_set': date_report_set,
    }
    return render(request, 'engineer/show_unforwarded_reports.html', context)


@login_required
@permission_required('engineer.full_control', raise_exception=True)
def show_forwarded_reports(request):
    """Відображення відправлених звітів"""    
    
    reports_forwarded = models.Report.objects.filter(checked=True).order_by('date')
    
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    date = request.GET.get('date')
    
    # radio true - diapason, false - concrete date
    radio = True

    if from_date and to_date:
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)
        reports_forwarded = reports_forwarded.filter(date__range = [from_date_correct, to_date_correct])

    if date:
        reports_forwarded = reports_forwarded.filter(date = correct_date(date))
        radio = False
    

    date_report_set = []
    reports_date = reports_forwarded.values('date').annotate(total=Count('id'))
    for report_date in reports_date:
        date = report_date['date'].strftime("%Y-%m-%d")
        queryset_rep = reports_forwarded.filter(date=date).select_related('filled_up')
        reports_set = []
        for query in queryset_rep:
            report_id = query.id
            driver = query.filled_up.full_name()
            brigade_name = query.filled_up.brigade_name
            machines = []
            for machine in query.machinereport_set.values('name', 'fuel', 'motohour', 'breakage', 'breakage_info'):
                
                name = machine['name']
                fuel = machine['fuel']
                motohour = machine['motohour']
                breakage = "Є поломка" if machine['breakage'] else "Поломок не було"
                if breakage == "Є поломка":
                    if machine['breakage_info']:
                        breakage += f"<br>Інформація: {machine['breakage_info']}"
                    else:
                        breakage = f"<br>Інформація про поломку відсутня"
                
                machines_info = {
                    'machine_short_name': name,
                    'machine_full_name': name,
                    'fuel': fuel,
                    'motohour': motohour,
                    'breakage': breakage,
                }

                machines.append(machines_info)

            reports_set.append({'report_id': report_id, 'driver': driver, 'brigade_name': brigade_name, 'machines': machines})
        date_report_set.append({'date': date, 'report_info': reports_set})


    context = {
        'from_date': from_date,
        'to_date' : to_date,
        'date': date,
        'radio': radio,
        'date_report_set': date_report_set,
    }
    return render(request, 'engineer/show_forwarded_reports.html', context)



@login_required
@permission_required('engineer.full_control', raise_exception=True)
def show_drivers(request):
    """ Старші водії """

    drivers = SeniorDriver.objects.all().order_by('brigade_name').select_related('user')
    context = {
        'drivers': drivers
    }
    return render(request, 'engineer/show_drivers.html', context)


@login_required
@permission_required('engineer.full_control', raise_exception=True)
def show_drivers_detail(request, username):
    """ Деталбна інформація про водія """

    driver = SeniorDriver.objects.select_related('user').get(user__username=username)
    

    reports_driver = models.Report.objects.filter(filled_up=driver).values('id', 'date')
    machine_reports_all = MachineReport.objects.filter(Q(report_id__in = [o["id"] for o in reports_driver])).values('name', 'fuel', 'motohour','breakage', 'breakage_info', 'report_id')

    
    for report in reports_driver:
        report["machines"] = []
        for machine_report in machine_reports_all.filter(report_id=report["id"]):
            report["machines"].append({'machine': machine_report["name"], 'motohour': machine_report["motohour"], 'fuel': machine_report["fuel"]})


    context = {
        'driver': driver,
        'reports_driver': reports_driver,
        'report_set': reports_driver, 
    }
    return render(request, 'engineer/show_driver_detail.html', context)

 
@login_required
@permission_required('engineer.full_control', raise_exception=True)
def work_days(request):
    """ Графік роботи / звітність """

    context = {}
    return render(request, 'engineer/work_days.html', context)


@login_required
@permission_required('engineer.full_control', raise_exception=True)
def show_fix_machines(request):
    """ Машини які перебувають/перебували у ремонті """

    engineer = set_engineer(request.user)
    if request.method == "POST":
        machine_id = request.POST.get('breakage_machine_id')
        
        machine = models.Machine.objects.get(pk=machine_id)
        
        machine.breakage = False
        machine.breakage_info = f"{machine.breakage_info}\nUPDATE: Машина була починена {datetime.date.today()}"
        machine.fix_date = datetime.date.today()
        machine.fix_by = engineer.full_name()
        
        machine.save()

    breakage_machines = Machine.objects.filter(breakage=True).order_by('-brigade')
    context = {
        'breakage_machines': breakage_machines
    }
    return render(request, 'engineer/fix_machines.html', context)


@login_required
@permission_required('engineer.full_control', raise_exception=True)
def all_machines(request):
    
    machiness = models.Machine.objects.all().values('name', 'number_machine', 'inventory_number', 'id')
    query = request.GET.get('q')
    if query:
        machiness = machiness.filter(
            Q(name__icontains=query) | Q(inventory_number__icontains=query) |
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
    return render(request, 'engineer/machines.html', context=context)


# ПРАВИЛЬНА ДАТА
def correct_date(date):
    date_list = date.split('/')
    date_correct = f"{date_list[2]}-{date_list[0]}-{date_list[1]}"
    return date_correct

def set_engineer(user):
    if user.is_superuser:
        return Engineer.objects.all()[0]
    return user.engineer