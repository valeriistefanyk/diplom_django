from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

from main._helper_func import _whoisit, _status


# request is django.core.handlers.wsgi.WSGIRequest class
def home(request):
    return render(request, 'main/home.html')



def mylogin(request):

    user = request.user
    context = {}
    # login and permission check start
    if request.user.is_authenticated:
        return redirect_on_right_page(request, user)


    context = {
        'message': ''
    }
    if request.method == 'POST':

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":
            
            this_user = authenticate(username=utxt, password=ptxt)
            if this_user != None:
                login(request, this_user)
                return redirect_on_right_page(request, this_user)

            context['message'] = 'Не правильний логін або пароль!'

    return render(request, 'main/login.html', context)


def mylogout(request):

    logout(request)
    return redirect('mylogin')


### допоможні методи ###
def redirect_on_right_page(request, user):

    next_value = request.POST.get('next')
    print(next_value)
    if next_value:
        return redirect(next_value)

    if user.is_superuser:
        return redirect('/admin/')
    if user.has_perm('senior_driver.full_control'):
        return redirect('driver:home-page')
    if user.has_perm('engineer.full_control'):
        return redirect('engineer:home-page')
    if user.has_perm('director.full_control'):
        return redirect('director:home-page')
    return redirect('/')