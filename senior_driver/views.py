from django.shortcuts import render, redirect, get_object_or_404
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
def show_my_reports_detail(request, report_id):
    """ Детально про звіт """
    
    driver = set_driver(request.user)

    try:
        report = Report.objects.select_related('filled_up', 'filled_up__user').get(pk=report_id)
    except:
        raise Http404("Звіт не знайдений")
    if report.filled_up != driver:
        raise Http404("Звіти зробив інший машиніст. Ви не маєте доступа до цього звіту!")


    machinereports = MachineReport.objects.filter(report_id=report.id).select_related('machine', 'machine__machine')

    data_for_js = []

    breakage = False
    
    for machinereport in machinereports:
        if machinereport.breakage:
            breakage = True

        if machinereport.latFld and machinereport.lngFld:
            data = [machinereport.name, machinereport.latFld, machinereport.lngFld]
            data_for_js.append(data)
    
    
    if len(data_for_js) > 1:
        lat_arr = [el[1] for el in data_for_js]
        lng_arr = [el[2] for el in data_for_js]
        center_lat = sum(lat_arr)/len(lat_arr)
        center_lng = sum(lng_arr)/len(lng_arr)
        center = {"lat": center_lat, "lng": center_lng}
    elif len(data_for_js) == 1:
        center = {"lat": data_for_js[0][1], "lng": data_for_js[0][2]}
    else:
        center = {"lat": 50.443165, "lng": 30.485434}
    
    context = {
        'report': report,
        'machinereports': machinereports,
        'data_for_js': data_for_js,
        'center_map': center,
        'breakage': breakage
    }
    
    return render(request, 'senior-driver/my_reports_detail.html', context)


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
    
    
    date = request.POST.getlist('date')[0] if request.POST.getlist('date') else None

    context = {}
    
    if request.POST.get('selectMachines'):
        machine_id_list = list(map(lambda el: int(el), request.POST.getlist('choices')))
        machines = Machine.objects.filter(id__in=machine_id_list)

        context = {
            'date': date,
            'machines': machines,
            'machine': machines[0] if machines else None,
        }
    
    if request.POST.get('sendData'):
        
        report = get_or_create_report(request.POST.get('report_id'), date, request)
                
        fuel = request.POST.get('fuel')
        motohour = request.POST.get('motohour')
        machine_breakage = request.POST.get('breakage')
        machine_breakage_info = request.POST.get('breakage_info')
        

        this_machine_id = int(request.POST.get('this_machine'))
        
        machine_id_list = list(map(lambda el: int(el), request.POST.getlist('choices')))
        machine_id_list.remove(this_machine_id) 
        
        current_machine = Machine.objects.get(id=this_machine_id)

        current_machine.work_days += 1
        current_machine.last_used_data = date
        
        machine_report = MachineReport.objects.create(
            report = report,
            name = current_machine.name + ' №' + current_machine.number_machine,
            machine = current_machine,
            motohour = motohour,
            fuel = fuel,
        )

        if request.POST.get('latFld') and request.POST.get('lngFld'):
            machine_report.latFld = request.POST.get('latFld')
            machine_report.lngFld = request.POST.get('lngFld')

        if request.POST.get('breakage'):
            current_machine.breakage = True
            current_machine.breakage_info = machine_breakage_info
            current_machine.breakage_date = date

            machine_report.breakage = True
            machine_report.breakage_info = machine_breakage_info
            machine_report.breakage_date_start = date


        current_machine.save()
        machine_report.save()

        machines = Machine.objects.filter(id__in=machine_id_list)

        print(f"{date}\n{fuel}\n{motohour}\n{machine_breakage}\n{machine_breakage_info}\n")
        if not machines:
            return render(request, 'senior-driver/home_page.html', {'message': 'Звіт створений'})
        
        context = {
            'report_id': report.id,
            'date': date,
            'machines': machines,
            'machine': machines[0],
        }

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


def get_or_create_report(report_id, date, request):
    if report_id:
        report = Report.objects.get(id= report_id)
        print('report: ', report, '. id = ', report.id)
        return report
        
    else:
        filled_up = set_driver(request.user)
        report = Report.objects.create(filled_up=filled_up, date=date) 

        print('report created, report_id: ', report.id)

        return report