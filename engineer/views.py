from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.db.models import Count

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

    machines_all = Machine.objects.values('id', 'machine__name', 'number_machine', 'inventory_number', 'breakage', 'breakage_info', 'fix_date')
    date_report_set = []
    reports_date = reports_unforwarded.values('date').annotate(total=Count('id'))
    for report_date in reports_date:
        date = report_date['date'].strftime("%Y-%m-%d")
        queryset_rep = reports_unforwarded.filter(date=date).select_related('filled_up')
        reports_set = []
        for query in queryset_rep:
            report_id = query.id
            driver = query.filled_up.full_name()
            brigade_name = query.filled_up.brigade_name
            machines = []
            for machine in query.machinereport_set.values():
                m = machines_all.get(id=machine['machine_id'])
                machine_short_name =  f"{m['machine__name']} #{m['number_machine']}"
                machine_full_name =  f"{m['machine__name']} #{m['number_machine']} [IN{m['inventory_number']}]"
                fuel = machine['fuel']
                motohour = machine['motohour']
                
                breakage_from_report = machine['breakage']
                if breakage_from_report:
                    breakage = "Є поломка"
                    if not m['breakage']:
                        breakage += f"<br>Оновлення: машина була починена {m['fix_date']}"
                    elif m['breakage_info']:
                        breakage += f"<br>Інформація: {m['breakage_info']}"
                    else:
                        breakage = f"<br>Інформація про поломку відсутня"
                else:
                    breakage = "Поломки не було"
                        
                
                machines_info = {
                    'machine_short_name': machine_short_name,
                    'machine_full_name': machine_full_name,
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
    

    machines_all = Machine.objects.values('id', 'machine__name', 'number_machine', 'inventory_number', 'breakage_info')
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
            for machine in query.machinereport_set.values():
                m = machines_all.get(id=machine['machine_id'])
                machine_short_name =  f"{m['machine__name']} #{m['number_machine']}"
                machine_full_name =  f"{m['machine__name']} #{m['number_machine']} [IN{m['inventory_number']}] "
                fuel = machine['fuel']
                motohour = machine['motohour']
                breakage = "Є поломка" if machine['breakage'] else "Поломок не було"
                if breakage == "Є поломка":
                    if m['breakage_info']:
                        breakage += f"<br>Інформація: {m['breakage_info']}"
                    else:
                        breakage = f"<br>Інформація про поломку відсутня"
                
                machines_info = {
                    'machine_short_name': machine_short_name,
                    'machine_full_name': machine_full_name,
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

    drivers = SeniorDriver.objects.all().order_by('brigade_name')
    context = {
        'drivers': drivers
    }
    return render(request, 'engineer/show_drivers.html', context)


@login_required
@permission_required('engineer.full_control', raise_exception=True)
def show_drivers_detail(request, username):
    """ Деталбна інформація про водія """

    driver = get_object_or_404(SeniorDriver, user__username=username)
    reports_driver = models.Report.objects.filter(filled_up=driver)
    machines_driver = models.Machine.objects.filter(brigade=driver)
    report_set = []
    for report in reports_driver:
        machine_reports = MachineReport.objects.filter(report=report)
        data = []
        for machine_report in machine_reports:
            data.append({'machine': machine_report.machine, 'motohour': machine_report.motohour, 'fuel': machine_report.fuel})
        report_set.append({'id': report.id, 'date': report.date, 'data': data})


    context = {
        'driver': driver,
        'reports_driver': reports_driver,
        'report_set': report_set, 
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
        print(machine)

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

def set_engineer(user):
    if user.is_superuser:
        return Engineer.objects.all()[0]
    return user.engineer