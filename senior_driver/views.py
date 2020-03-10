from django.shortcuts import render, redirect

def hello_mess(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    return render(request, 'senior-driver/home_page.html', context={})

def about(request):

# login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end


    return render(request, 'senior-driver/about.html')