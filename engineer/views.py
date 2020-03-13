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

    reports = models.Report.objects.all()
    context = {
        'reports': reports
    }
    
    return render(request, 'engineer/show_reports.html', context)