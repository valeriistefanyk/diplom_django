from django.shortcuts import render

def hello_mess(request):
    return render(request, 'engineer/home_page.html')