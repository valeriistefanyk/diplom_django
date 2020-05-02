from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from machines.models import Machine, MachineName
from engineer.models import Report, Engineer, MachineReport
from senior_driver.models import SeniorDriver

import datetime
import json


@login_required
@permission_required('director.full_control', raise_exception=True)
def home_page(request):
    """ Стартова сторінка директора """
    
    return render(request, 'director/home_page.html')


@login_required
@permission_required('director.full_control', raise_exception=True)
def show_reports(request):
    """ Звіти які передані від інженера """
    
    reports = Report.objects.filter(checked=True).select_related('filled_up', 'filled_up__user').order_by('-date')
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if from_date and to_date:
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)
        reports = reports.filter(date__range = [from_date_correct, to_date_correct])
    


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
                name =  machine["name"]
                fuel = machine['fuel']
                motohour = machine['motohour']
                breakage = "True" if machine['breakage'] else "False"
                breakage_info = machine['breakage_info'] if machine['breakage_info'] else ''
                
                machines_info = {
                    'machine_short_name': name,
                    'machine_full_name': name,
                    'fuel': fuel,
                    'motohour': motohour,
                    'breakage': breakage,
                    'breakage_info': breakage_info
                }

                machines.append(machines_info)

            reports_set.append({'report_id': report_id, 'driver': driver, 'brigade_name': brigade_name, 'machines': machines})
        date_report_set.append({'date': date, 'report_info': reports_set})
    # попробуем сортировку по дням (конец кода)
    
    context = {
        'from_date': from_date,
        'to_date' : to_date,
        'date_report_set': date_report_set,
    }
    return render(request, 'director/show_reports.html', context=context)


@login_required
@permission_required('director.full_control', raise_exception=True)
def show_report_detail(request, report_id):
    
    try:
        report = Report.objects.select_related('checked_by', 'filled_up', 'filled_up__user', 'checked_by__user').get(pk=report_id)
    except:
        raise Http404("Звіт не знайдений")
    
    if report.checked == False:
        raise Http404("Звіт ще не був переданий Вам. Інформація про цей звіт поки не доступна!")

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
    return render(request, 'director/detail_report.html', context=context)


@login_required
@permission_required('director.full_control', raise_exception=True)
def show_statistics(request):
    """ Перегляд статистики """

    drivers = SeniorDriver.objects.all().order_by('brigade_name').select_related('user')
    data_report = {
        'names': drivers.values_list('brigade_name', flat=True)
    }

    context = {
        'drivers': drivers,
    }
    return render(request, 'director/statistics.html', context=context)


@login_required
@permission_required('director.full_control', raise_exception=True)
def brigade_statistic(request, driver_id):
    """ Статистика по кожній бригаді """

    status = { 'month': 'month', 'diapazon': 'diapazon' }

    driver = get_object_or_404(SeniorDriver, pk=driver_id)

    machinereports = MachineReport.objects.all().select_related('report')

    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    month = request.GET.get('month')

    radio_current = status['diapazon']

    if from_date and to_date:
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)

        machinereports = machinereports.filter(report__date__range = [from_date_correct, to_date_correct])
    
    if month:
        machinereports = machinereports.filter(report__date__year=month.split('/')[1], report__date__month=month.split('/')[0])
        radio_current = status['month']
        # some_date = month.split('/')
        # month2 = f"{calendar.month_name[int(some_date[0])]}, {some_date[1]}"

    # distinct = machinereports.values('machine').annotate(machine_count=Count('machine'))
    # machines = Machine.objects.filter(id__in=[item['machine'] for item in distinct])

    # machines = machinereports.values('name').annotate(name_count=Count('name')).order_by('-name_count')

    data = None
    count_machine = None
    
    if from_date and to_date:
        data, count_machine = get_chart_data(machinereports, from_date_correct, to_date_correct)

    if month:
        data, count_machine = get_chart_data(machinereports, month=month)

    context = {
        'from_date': from_date,
        'to_date' : to_date,
        'month': month,
        'driver': driver,
        'radio_current': radio_current,

        'count_machine': count_machine,
        'data': data, 
    }
    return render(request, 'director/brigade_statistic.html', context=context)


@login_required
@permission_required('director.full_control', raise_exception=True)
def show_employees(request):
    """ Інформація про працівників """
    engineer = Engineer.objects.all().select_related('user')
    drivers = SeniorDriver.objects.all().order_by('brigade_name').select_related('user')

    engineers_info = [{'avatar': eng.avatar, 'full_name': eng.full_name(), 'email': eng.user.email, 'phones': eng.phones()} for eng in engineer]
    drivers_info = [{'avatar': drvr.avatar, 'brigade': drvr.brigade_name, 'full_name': drvr.full_name(), 'email': drvr.user.email, 'phones': drvr.phones()} for drvr in drivers]

    context = {
        'engineers': engineers_info,
        'drivers': drivers_info,
    }
    return render(request, 'director/employees.html', context)


@login_required
@permission_required('director.full_control', raise_exception=True)
def all_machines(request):
    
    machiness = Machine.objects.all()
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
    return render(request, 'director/machines.html', context=context)


# ПРАВИЛЬНА ДАТА
def correct_date(date):
    date_list = date.split('.')
    date_correct = f"{date_list[2]}-{date_list[1]}-{date_list[0]}"
    return date_correct


def get_chart_data(machinereports, from_date = None, to_date = None, month = None):

    # timestamps = [datetime.datetime(2016, 11, 21, 0, 0), datetime.datetime(2016, 11, 22, 0, 0), datetime.datetime(2016, 11, 23, 0, 0)]
    # labels = [d.strftime('%Y-%d-%m') for d in timestamps]
    machines_data = []

    machines = machinereports.values('name').annotate(name_count=Count('name')).order_by('-name_count')
    id = 0
    if from_date and to_date:
        for machine in machines:

            machines_range_date = machinereports.filter(name=machine['name'], report__date__range=(from_date, to_date)).order_by('report__date')

            data_fuel = []
            data_motohour = []
            labels = []

            for element in machines_range_date:
                labels.append(element.report.date)
                data_fuel.append(element.fuel)
                data_motohour.append(element.motohour)
            id += 1
            machines_data.append({'name': machine['name'], 'count': machine['name_count'], 'id': id, 'labels': labels, 'data_fuel': data_fuel, 'data_motohour': data_motohour})
        count_machine = machines.count()
    
    elif month:
        for machine in machines:
    
            machines_range_date = machinereports.filter(name=machine['name'], report__date__year=month.split('/')[1], report__date__month=month.split('/')[0]).order_by('report__date')

            data_fuel = []
            data_motohour = []
            labels = []

            for element in machines_range_date:
                labels.append(element.report.date)
                data_fuel.append(element.fuel)
                data_motohour.append(element.motohour)
            id += 1
            machines_data.append({'name': machine['name'], 'count': machine['name_count'], 'id': id, 'labels': labels, 'data_fuel': data_fuel, 'data_motohour': data_motohour})
        count_machine = machines.count()

    return machines_data, count_machine