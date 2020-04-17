from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
import json
from django.db.models import Count

from machines.models import Machine
from engineer.models import Report, Engineer
from senior_driver.models import SeniorDriver


@login_required
@permission_required('director.full_control', raise_exception=True)
def home_page(request):
    """ Стартова сторінка директора """
    
    return render(request, 'director/home_page.html')


@login_required
@permission_required('director.full_control', raise_exception=True)
def show_reports(request):
    """ Звіти які передані від інженера """
    
    reports = Report.objects.filter(checked=True)
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if from_date and to_date:
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)
        reports = reports.filter(date__range = [from_date_correct, to_date_correct])
        print(reports)
    


    machines_all = Machine.objects.values('id', 'machine__name', 'number_machine', 'inventory_number', 'breakage_info')
    # попробуем сортировку по дням (начало кода)
    date_report_set = []
    reports_date = reports.values('date').annotate(total=Count('id'))
    for report_date in reports_date:
        date = report_date['date'].strftime("%Y-%m-%d")
        queryset_rep = reports.filter(date=date).select_related('filled_up')
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
                breakage = "True" if machine['breakage'] else "False"
                breakage_info = m['breakage_info'] if m['breakage_info'] else ''
                
                machines_info = {
                    'machine_short_name': machine_short_name,
                    'machine_full_name': machine_full_name,
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
def show_statistics(request):
    """ Графіки """

    reports = Report.objects.all()
    drivers = SeniorDriver.objects.all().order_by('brigade_name')
    data_report = {
        'names': drivers.values_list('brigade_name', flat=True)
    }

    ########## DATA FOR CHARTS START ##########
    
    
    #######
    # g_drivers = SeniorDriver.objects.all()
    # g_reports_driver = []
    # for g_driver in g_drivers:
    #     g_reports_driver.append(Report.objects.filter(filled_up=g_driver))
    # g_machines = []
    # for g_report_driver in g_reports_driver:
    #     g_machines.append(g_report_driver)

    ## названия всех машин
    # def machines_of_driver(reports_of_drivers):
    #     machines = []
    #     for report in reports_of_drivers:
    #         machines_set = report.machinereport_set.values()
    #         for machine in machines_set:
    #             machine_concrete = Machine.objects.get(pk=machine['machine_id'])
    #             machine_name = machine_concrete.machine.name + machine_concrete.number_machine
    #             if not machine_name in machines:
    #                 machines.append(machine_name)
    #     return machines
    
    # g_reports_drivers = []
    # g_drivers = SeniorDriver.objects.all()
    # for g_driver in g_drivers:
    #     g_reports_driver.append(Report.objects.filter(filled_up=g_driver))

    # data = []   
    # for reports_driver in g_reports_drivers:
    #     data.append(machines_of_driver(reports_driver))


    # addColumns_list = [machine for machine in machines_of_driver(reports_of_drivers)]
    #######

    
    # higonov (№5)
    # values_data = []
    # higonov = SeniorDriver.objects.get(user__username='higonov')
    # reports_higonov = Report.objects.filter(filled_up=higonov)

    # m1 = reports_higonov[0].machine
    # m2 = reports_higonov[0].machine
    
    # reports_higonov_m1 = reports_higonov.filter(machine=m1)
    # reports_higonov_m2 = reports_higonov.filter(machine=m2)

    # reports_higonov_m1.filter(date__range = ['2020-02-23', '2020-03-30'])
    # reports_higonov_m2.filter(date__range = ['2020-02-23', '2020-03-30'])
    
    
    # addColumns = [m1.machine.name + ' #' + m1.number_machine, m2.machine.name + ' #' + m2.number_machine]
    # addRows = []
    
    # for i in range(0, reports_higonov_m1.count()):
    #     addRows.append([reports_higonov_m1[i].date, 
    #                     reports_higonov_m1[i].motohour, 
    #                     reports_higonov_m2[i].motohour, 
    #                     [
    #                         reports_higonov_m1[i].machine.machine.name + ' #' + reports_higonov_m1[i].machine.number_machine,
    #                         reports_higonov_m1[i].date.strftime('%b %d, %Y'),
    #                         reports_higonov_m1[i].fuel,
    #                         reports_higonov_m1[i].motohour
    #                     ],
    #                     [
    #                         reports_higonov_m2[i].machine.machine.name + ' #' + reports_higonov_m2[i].machine.number_machine,
    #                         reports_higonov_m2[i].date.strftime('%b %d, %Y'),
    #                         reports_higonov_m2[i].fuel,
    #                         reports_higonov_m2[i].motohour
    #                     ],
    #                 ])

    
    # addRows = [['12-02-2020', 20, 30], ["new Date(2020, 0)", 0, 0], ...]

    ########## DATA FOR CHARTS END ##########


    context = {
        'reports': reports,
        'drivers': drivers,
        
        # 'addColumns': addColumns,
        # 'addRows': addRows
    }
    return render(request, 'director/statistics.html', context=context)


#### TEST STATISTICS SHOW (END) ####
@login_required
@permission_required('director.full_control', raise_exception=True)
def test_show_statistics(request):
    
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
    return render(request, 'director/test_statistics.html', context=context)
#### TEST STATISTICS SHOW (END) ####



@login_required
@permission_required('director.full_control', raise_exception=True)
def show_employees(request):
    """ Інформація про працівників """

    engineers_info = [{'avatar': eng.avatar, 'full_name': eng.full_name(), 'email': eng.user.email, 'phones': eng.phones()} for eng in Engineer.objects.all()]
    drivers_info = [{'avatar': drvr.avatar, 'brigade': drvr.brigade_name, 'full_name': drvr.full_name(), 'email': drvr.user.email, 'phones': drvr.phones()} for drvr in SeniorDriver.objects.all().order_by('brigade_name')]

    context = {
        'engineers': engineers_info,
        'drivers': drivers_info,
    }
    return render(request, 'director/employees.html', context)




# ПРАВИЛЬНА ДАТА
def correct_date(date):
    date_list = date.split('/')
    date_correct = f"{date_list[2]}-{date_list[0]}-{date_list[1]}"
    return date_correct