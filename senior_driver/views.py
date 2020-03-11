from django.shortcuts import render, redirect
from django.http import Http404


def hello_mess(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('driver.view_driver' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    return render(request, 'senior-driver/home_page.html', context={})

def about(request):

# login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if not ('driver.view_driver' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")

    return render(request, 'senior-driver/about.html')