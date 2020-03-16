from django.shortcuts import render, redirect
from django.http import Http404

from machines.models import Machine
from engineer.models import Report
import datetime



def home_page(request):

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

    if not request.user.is_superuser:
        can_use_machines = Machine.objects.filter(
            brigade=request.user.seniordriver).exclude(breakage=True)
    else:
        can_use_machines = Machine.objects.all()[:5]
        
    context = {
        'can_use_machines': can_use_machines,
        'date_today': datetime.date.today().strftime("%Y-%m-%d")
    }

    if request.method == "POST":
        
        if not request.user.is_superuser:
            filled_up = request.user.seniordriver
            date = request.POST.get('date')
            motohour = request.POST.get('motohour')
            fuel = request.POST.get('fuel')

            machine_id = request.POST.get('machine')
            machine = Machine.objects.get(pk=machine_id)
            
            breakage = True if request.POST.get('breakage') == 'on' else False

            # print(
            #     f"filled up: {filled_up}\ndate: {date}\nmotohour: {motohour}\nfuel: {fuel}\nmachine id: {machine_id}\nbreakage: {breakage}"
            # )

            if breakage:
                machine.breakage = True
                machine.save()

            report = Report.objects.create(filled_up=filled_up, date=date, motohour=motohour, fuel=fuel, machine=machine, breakage=breakage)
            

        return redirect('driver:home-page')

    return render(request, 'senior-driver/make_report.html', context)



def show_my_reports(request):
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    my_reports = Report.objects.filter(filled_up__user=request.user)
    context = {
        'my_reports': my_reports
    }
    
    return render(request, 'senior-driver/my_reports.html', context)



def show_machines(request):
    
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        # return redirect(reverse('home', kwargs={ 'message': FooBar }))
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    

    if not request.user.is_superuser:
        my_machines = Machine.objects.filter(brigade=request.user.seniordriver)
    else:
        my_machines = Machine.objects.all()

    
    context = {
        'my_machines': my_machines.filter(breakage=False),
        'my_machines_broken': my_machines.filter(breakage=True),
    }

    return render(request, 'senior-driver/my_machines.html', context)