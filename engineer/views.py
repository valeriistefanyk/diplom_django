from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Count

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
def show_unforwarded_reports(request):
    """Відображення невідправлених звітів """
    
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
            if not request.user.is_superuser:
                report.checked = True
                report.save()
            else:
                print(report)
            

    reports_unforwarded = models.Report.objects.filter(checked=False).order_by('date')

    machines_all = Machine.objects.values('id', 'machine__name', 'number_machine', 'inventory_number', 'breakage_info')
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
        'date_report_set': date_report_set,
    }
    return render(request, 'engineer/show_unforwarded_reports.html', context)


def show_forwarded_reports(request):
    """Відображення відправлених звітів"""
    
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    
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