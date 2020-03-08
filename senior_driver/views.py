from django.shortcuts import render

def hello_mess(request):
    return render(request, 'senior-driver/home_page.html', context={})

def about(request):
    return render(request, 'senior-driver/about.html')