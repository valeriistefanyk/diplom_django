from django.shortcuts import render


def hello_mess(request):
    return render(request, 'director/home_page.html')