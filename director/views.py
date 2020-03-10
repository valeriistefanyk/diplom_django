from django.shortcuts import render, redirect


def hello_mess(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    return render(request, 'director/home_page.html')