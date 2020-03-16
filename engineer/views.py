from django.shortcuts import render, redirect
from django.http import Http404

from engineer import models


def hello_mess(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    
    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    return render(request, 'engineer/home_page.html')

def showRaports(request):
    """Відображення звіту для інженера"""
    
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('engineer.view_engineer' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    if request.method == "POST":
        checked = request.POST.get('checked')
        report_id = request.POST.get('report_id')
        
        if checked == "True":
            report = models.Report.objects.get(pk=report_id)
            report.checked = True
            report.save()
            print(f"CHECKED: {checked}\nREPORT ID: {report_id}\nREPORT MODEL: {report}\nREPORT CHECKED BEFORE: {report.checked}")

    reports = models.Report.objects.all()

    context = {
        'reports': reports,
        'reports_forwarded': reports.filter(checked=True),
        'reports_unforwarded': reports.filter(checked=False),
    }
    return render(request, 'engineer/show_reports.html', context)


def show_drivers(request):

    from senior_driver.models import SeniorDriver

    drivers = SeniorDriver.objects.all()
    context = {
        'drivers': drivers
    }
    return render(request, 'engineer/show_drivers.html', context)