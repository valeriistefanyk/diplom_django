from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

# request is django.core.handlers.wsgi.WSGIRequest class
def home(request):


    if request.user.is_authenticated:
        user = request.user
        return HttpResponse('Hello ' + user.username + '.<br><a href="/logout">LOGOUT</a>')
    return HttpResponse('Ви не аутентифіковані, для аутентифікації перейдіть будь ласка на сторінку /login/')

def mylogin(request):
    
    if request.method == 'POST':

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":
            
            user = authenticate(username=utxt, password=ptxt)
            if user != None:
                login(request, user)
                return redirect('home')
            return HttpResponse('Hello some user!')

    return render(request, 'main/login.html')


def mylogout(request):
    logout(request)
    return redirect('mylogin')