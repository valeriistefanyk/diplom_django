from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

from main._helper_func import _whoisit, _status


def home(request):

    user = request.user
    context = {}
    
    if request.POST.get('entrance'):
        return redirect_on_right_page(request, request.user)

    if request.method == 'POST':

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":
            
            this_user = authenticate(username=utxt, password=ptxt)
            if this_user != None:
                login_user = login(request, this_user)
                return redirect_on_right_page(request, this_user)

            context['message'] = 'Не правильний логін або пароль!'


    return render(request, 'main/home.html', context)



def mylogout(request):

    logout(request)
    return redirect('/')


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