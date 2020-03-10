from django.shortcuts import render, redirect

from engineer import models


def hello_mess(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    return render(request, 'engineer/home_page.html')

def showRaports(request):
    """Відображення звіту для інженера"""
    
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end


    raports = models.Report.objects.all()
    context = {
        'raports': raports
    }
    
    return render(request, 'engineer/show_raports.html', context)