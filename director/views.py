from django.shortcuts import render, redirect
from django.http import Http404

from engineer.models import Report, Engineer
from senior_driver.models import SeniorDriver


def hello_mess(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('director.view_director' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    return render(request, 'director/home_page.html')


def show_reports(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('director.view_director' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    context = {
        'reports': Report.objects.filter(checked=True)
    }
    return render(request, 'director/show_reports.html', context=context)



def show_statistics(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('director.view_director' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    context = {

    }

    return render(request, 'director/statistics.html', context=context)



def show_employees(request):
    
    engineers_info = [{'full_name': eng.full_name(), 'email': eng.user.email, 'phones': eng.phones()} for eng in Engineer.objects.all()]
    drivers_info = [{'brigade': drvr.brigade_name, 'full_name': drvr.full_name(), 'email': drvr.user.email, 'phones': drvr.phones()} for drvr in SeniorDriver.objects.all()]

    context = {
        'engineers': engineers_info,
        'drivers': drivers_info,
    }
    
    return render(request, 'director/employees.html', context)