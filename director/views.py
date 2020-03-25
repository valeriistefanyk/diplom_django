from django.shortcuts import render, redirect
from django.http import Http404

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
    context = {
        'reports': reports,
        'drivers': drivers,
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
    drivers_info = [{'avatar': drvr.avatar, 'brigade': drvr.brigade_name, 'full_name': drvr.full_name(), 'email': drvr.user.email, 'phones': drvr.phones()} for drvr in SeniorDriver.objects.all()]

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