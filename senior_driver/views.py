from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Sum

from machines.models import Machine
from engineer.models import Report, MachineReport, Engineer
from director.models import Director
from senior_driver.models import SeniorDriver
import datetime


def test(request):
    return render(request, 'senior-driver/test4.html', context={})

@login_required
@permission_required('senior_driver.full_control', raise_exception=True)
def home_page(request):
    """ Початкова сторінка бригадира """

    return render(request, 'senior-driver/home_page.html', context={})


@login_required
@permission_required('senior_driver.full_control', raise_exception=True)
def about(request):
    
    driver = set_driver(request.user)
    engineers = Engineer.objects.all().select_related('user')
    directors = Director.objects.all().select_related('user')
    context = {
        'driver': driver,
        'engineers': engineers,
        'directors': directors,
    }
    return render(request, 'senior-driver/about_page.html', context)


@login_required
@permission_required('senior_driver.full_control', raise_exception=True)
def show_my_reports(request):
    """ Звіти старшого водія """
    
    driver = set_driver(request.user)
    my_reports = Report.objects.filter(filled_up=driver).order_by('-id')
    
    if request.GET.get('from') and request.GET.get('to'):
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)
        my_reports = my_reports.filter(date__range = [from_date_correct, to_date_correct])
    else:
        from_date = correct_date(my_reports.earliest('date').date, choise=2)
        to_date = correct_date(my_reports.latest('date').date, choise=2)

    
    # my_reports = add_machines(my_reports)

    context = {
        'from_date': from_date,
        'to_date' : to_date,
        'my_reports': my_reports
    }
    return render(request, 'senior-driver/my_reports.html', context)


@login_required
@permission_required('senior_driver.full_control', raise_exception=True)
def show_machines(request):
    """ Машини які належать машиністу """
    
    driver = set_driver(request.user)
    my_machines = Machine.objects.filter(brigade=driver).select_related('machine')
    
    context = {
        'my_machines': my_machines.all(),
    }

    return render(request, 'senior-driver/my_machines.html', context)


@login_required
@permission_required('senior_driver.full_control', raise_exception=True)
def make_report(request):
    """ Створення звіту """

    driver = set_driver(request.user)
    
    all_machines = Machine.objects.filter(brigade=driver)

    can_use_machines = all_machines.filter(breakage=False)
    broken_machines = all_machines.filter(breakage=True).values('id', 'machine__name', 'number_machine', 'inventory_number')

    days, count = 30, 5
    last_used_machines = can_use_machines.filter(
            last_used_data__range=[datetime.date.today() - datetime.timedelta(days), datetime.date.today()]
        ).values('id', 'machine__name', 'number_machine', 'inventory_number'
        ).annotate(days=Sum('work_days')
        ).order_by('-days')[:count]

    long_used_machines = can_use_machines.filter(
            ~Q(id__in=[o["id"] for o in last_used_machines])
        ).values('id', 'machine__name', 'number_machine', 'inventory_number')

    context = {
        'broken_machines': broken_machines,
        'last_used_machines': last_used_machines,
        'long_used_machines': long_used_machines,
        'date_today': datetime.date.today().strftime("%Y-%m-%d")
    }

    return render(request, 'senior-driver/make_report.html', context)


@login_required
@permission_required('senior_driver.full_control', raise_exception=True)
def make_report_fill(request):
    
    machine_id_list = list(map(lambda el: int(el), request.POST.getlist('choices')))
    machines = Machine.objects.filter(id__in=machine_id_list)
    date = request.POST.getlist('date')[0] if request.POST.getlist('date') else None

    context = {}
    
    if request.POST.get('selectMachines'):

        
        context = {
            'date': date,
            'machines': machines,
        }

    if request.POST.get('sendData'):

        machine_fuel_list = list(map(lambda el: float(el), request.POST.getlist('fuel')))
        machine_motohour_list = list(map(lambda el: int(el), request.POST.getlist('motohour')))
        machine_breakage_list = request.POST.getlist('breakage')
        machine_breakage_info_list = request.POST.getlist('breakage_info')
        for i in range(len(machine_breakage_list)):
            if machine_breakage_list[i] == 'on':
                machine_breakage_list[i-1] = "del"
        machine_breakage_list = list(filter(lambda el: el == 'on' or el == 'off', machine_breakage_list))


        # создать отчеты
        filled_up = set_driver(request.user)
        report = Report.objects.create(filled_up=filled_up, date=date) 
            
        all_info = list(zip(machines, machine_motohour_list, machine_fuel_list, machine_breakage_list, machine_breakage_info_list))
    
        for el in all_info:
            machine = Machine.objects.get(pk=el[0].id)
            machine.work_days += 1
            machine.last_used_data = date
            breakage = False
            if el[3] == 'on':
                breakage = True
                machine.breakage = breakage
                machine.breakage_info = el[4]
                machine.breakage_date = date
            
            machine.save()
            MachineReport.objects.create(
                report = report,
                name = el[0].name + ' №' + el[0].number_machine,
                machine = el[0],
                motohour = el[1],
                fuel = el[2],
                breakage = breakage,
                breakage_info = el[4]
            )
            
        return render(request, 'senior-driver/home_page.html', {'message': 'Звіт створений'})
        
    return render(request, 'senior-driver/make_report_fill.html', context)



### допоміжні методи ###
def correct_date(date, choise = 1):
    if choise == 1:
        date_list = date.split('/')
        date_correct = f"{date_list[2]}-{date_list[0]}-{date_list[1]}"
        return date_correct
    if choise == 2:
        return date.strftime("%m/%d/%Y")


def add_machines(reports):
    machines_all = Machine.objects.values('id', 'machine__name', 'number_machine', 'inventory_number', 'breakage_info')
    for report in reports:
        machines = []

        for machine in report.machinereport_set.values():
            
            m = machines_all.get(id=machine['machine_id'])
            machine_full_name =  f"{m['machine__name']} #{m['number_machine']} [IN{m['inventory_number']}] "
            fuel = machine['fuel']
            motohour = machine['motohour']
            if machine['breakage']:
                breakage = "Є несправність"
                breakage += f"<br>({m['breakage_info']})"  if m['breakage_info'] else ''
            else:
                breakage = "В робочому стані"
                
            
            machines_info = {
                'full_name': machine_full_name,
                'fuel': fuel,
                'motohour': motohour,
                'breakage': breakage,
            }
            machines.append(machines_info)
        report.machines = machines
    return reports


def set_driver(user):
    if user.is_superuser:
        return SeniorDriver.objects.all().select_related('user')[1]
    return user.seniordriver