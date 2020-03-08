from django.shortcuts import render

from engineer import models


def hello_mess(request):
    return render(request, 'engineer/home_page.html')

def showRaports(request):
    """Відображення звіту для інженера"""
    raports = models.Report.objects.all()
    context = {
        'raports': raports
    }
    
    return render(request, 'engineer/show_raports.html', context)