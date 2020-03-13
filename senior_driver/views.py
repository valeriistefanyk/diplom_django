from django.shortcuts import render, redirect
from django.http import Http404

from machines.models import Machine


def hello_mess(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    return render(request, 'senior-driver/home_page.html', context={})


def about(request):

# login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    return render(request, 'senior-driver/about_page.html')



def make_report(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    machines = Machine.objects.all()

    # todo change
    used_machines = machines[:5]
    context = {
        'used_machines': used_machines 
    }

    if request.method == "POST":
        # TODO: make post data
        print("METHOD POST")
        return redirect('driver:home-page')

    return render(request, 'senior-driver/make_report.html', context)