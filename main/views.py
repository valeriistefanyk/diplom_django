from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

from main._helper_func import _whoisit, _status


# request is django.core.handlers.wsgi.WSGIRequest class
def home(request):
    return render(request, 'main/home.html')


def redirect_on_right_page(request):

    user = request.user
    status = _whoisit(user)
    if status == _status['admin']:
        return redirect('/admin/')
    if status == _status['driver']:
        return redirect('driver:home-page')
    if status == _status['director']:
        return redirect('director:home-page')
     
    if status == _status['engineer']:
        return redirect('engineer:home-page')

    return redirect('home')


def mylogin(request):
    
    # login and permission check start
    if request.user.is_authenticated:
        return redirect_on_right_page(request)

    context = {
        'message': ''
    }
    if request.method == 'POST':

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":
            
            user = authenticate(username=utxt, password=ptxt)
            if user != None:
                login(request, user)
                # return redirect('redirect_on_right_page')
                return redirect_on_right_page(request)

            context['message'] = 'Не правильний логін або пароль!'

    return render(request, 'main/login.html', context)


def mylogout(request):

    logout(request)
    return redirect('mylogin')