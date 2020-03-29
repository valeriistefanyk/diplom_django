from django.shortcuts import render, redirect
from django.http import Http404
import json
from django.db.models import Count

from machines.models import Machine
from engineer.models import Report, Engineer
from senior_driver.models import SeniorDriver


# Стартова сторінка директора
def home_page(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('director.view_director' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    return render(request, 'director/home_page.html')


# Звіти які передані від інженера
def show_reports(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('director.view_director' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    reports = Report.objects.filter(checked=True)
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    
    if from_date and not to_date:
        pass
    
    if not from_date and to_date:
        pass

    if from_date and to_date:
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)
        reports = reports.filter(date__range = [from_date_correct, to_date_correct])
        print(reports)
    
    context = {
        'from_date': from_date,
        'to_date' : to_date,
        'reports': reports.order_by('date'),
    }
    return render(request, 'director/show_reports.html', context=context)


# Графіки
def show_statistics(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('director.view_director' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    reports = Report.objects.all()
    drivers = SeniorDriver.objects.all().order_by('brigade_name')
    data_report = {
        'names': drivers.values_list('brigade_name', flat=True)
    }

    ########## DATA FOR CHARTS START ##########
    
    
    # higonov (№5)
    values_data = []
    higonov = SeniorDriver.objects.get(user__username='higonov')
    reports_higonov = Report.objects.filter(filled_up=higonov)

    m1 = reports_higonov[0].machine
    m2 = reports_higonov[0].machine
    
    reports_higonov_m1 = reports_higonov.filter(machine=m1)
    reports_higonov_m2 = reports_higonov.filter(machine=m2)

    reports_higonov_m1.filter(date__range = ['2020-02-23', '2020-03-30'])
    reports_higonov_m2.filter(date__range = ['2020-02-23', '2020-03-30'])
    
    
    addColumns = [m1.machine.name + ' #' + m1.number_machine, m2.machine.name + ' #' + m2.number_machine]
    addRows = []
    
    for i in range(0, reports_higonov_m1.count()):
        addRows.append([reports_higonov_m1[i].date, 
                        reports_higonov_m1[i].motohour, 
                        reports_higonov_m2[i].motohour, 
                        [
                            reports_higonov_m1[i].machine.machine.name + ' #' + reports_higonov_m1[i].machine.number_machine,
                            reports_higonov_m1[i].date.strftime('%b %d, %Y'),
                            reports_higonov_m1[i].fuel,
                            reports_higonov_m1[i].motohour
                        ],
                        [
                            reports_higonov_m2[i].machine.machine.name + ' #' + reports_higonov_m2[i].machine.number_machine,
                            reports_higonov_m2[i].date.strftime('%b %d, %Y'),
                            reports_higonov_m2[i].fuel,
                            reports_higonov_m2[i].motohour
                        ],
                    ])

    
    # addRows = [['12-02-2020', 20, 30], ["new Date(2020, 0)", 0, 0], ...]

    ########## DATA FOR CHARTS END ##########


    context = {
        'reports': reports,
        'drivers': drivers,
        
        'addColumns': addColumns,
        'addRows': addRows
    }
    return render(request, 'director/statistics.html', context=context)


# Інформація про працівників
def show_employees(request):
    
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('director.view_director' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

    engineers_info = [{'avatar': eng.avatar, 'full_name': eng.full_name(), 'email': eng.user.email, 'phones': eng.phones()} for eng in Engineer.objects.all()]
    drivers_info = [{'avatar': drvr.avatar, 'brigade': drvr.brigade_name, 'full_name': drvr.full_name(), 'email': drvr.user.email, 'phones': drvr.phones()} for drvr in SeniorDriver.objects.all().order_by('brigade_name')]

    context = {
        'engineers': engineers_info,
        'drivers': drivers_info,
    }
    return render(request, 'director/employees.html', context)



#### TEST SHOW REPORTS START####
def test_show_reports(request):
    
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('director.view_director' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    reports = Report.objects.filter(checked=True)
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if from_date and to_date:
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)
        reports = reports.filter(date__range = [from_date_correct, to_date_correct])
        print(reports)
    



    # попробуем сортировку по дням (начало кода)
    date_report_set = []
    reports_date = reports.values('date').annotate(total=Count('id'))
    for report_date in reports_date:
        date = report_date['date']
        queryset_rep = reports.filter(date=date)
        reports_set = []
        for query in queryset_rep:
            report_id = query.id
            driver = query.filled_up.full_name()
            brigade_name = query.filled_up.brigade_name
            machines = []
            for machine in query.machinereport_set.values():
                m = Machine.objects.get(pk=machine['machine_id'])
                machines.append(f'{m.machine.name} #{m.number_machine}')
            reports_set.append({'report_id': report_id, 'driver': driver, 'brigade_name': brigade_name, 'machines': machines})
        date_report_set.append({'date': date, 'report_info': reports_set})
    # попробуем сортировку по дням (конец кода)
    
    data = get_data_json_reports(reports)

    context = {
        'from_date': from_date,
        'to_date' : to_date,
        'reports_json': data,
        'date_report_set': date_report_set,
    }
    return render(request, 'director/test_show_reports.html', context=context)

#### TEST SHOW REPORTS END ####


# ДЛЯ МОДАЛЬНОГО ОКНА
def get_data_json_reports(reports):
    from machines.models import Machine
    from django.core import serializers
    
    reports_object = []
    
    for report in reports:
        id = report.id
        filled_up = report.filled_up.full_name()
        brigade_name = report.filled_up.brigade_name
        date = report.date
        machinereports_set = list(report.machinereport_set.values())
        machinereport = []
        for machinereport_set in machinereports_set:
            machine = Machine.objects.get(pk=machinereport_set['machine_id'])
            
            breakage = 'True' if machine.breakage == True and machinereport_set['breakage'] == True else 'False'
            breakage_info = machine.breakage_info
            machinereport.append(
                {
                    'machine': machine.full_name(),
                    'fuel': machinereport_set['fuel'],
                    'motohour': machinereport_set['motohour'],
                    'breakage': breakage,
                    'breakage_info': breakage_info
                }
            )
        elements = {
            'id': id,
            'date': date.strftime("%Y-%m-%d"),
            'filled_up': filled_up,
            'brigade_name': brigade_name,
            'machines': machinereport,
        }
        
        reports_object.append(elements)

    return reports_object



# ПРАВИЛЬНА ДАТА
def correct_date(date):
    date_list = date.split('/')
    date_correct = f"{date_list[2]}-{date_list[0]}-{date_list[1]}"
    return date_correct