from django.shortcuts import render, redirect
from django.http import Http404

from machines.models import Machine
from engineer.models import Report, MachineReport
import datetime


def home_page(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

    return render(request, 'senior-driver/home_page.html', context={})



def about(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

    return render(request, 'senior-driver/about_page.html')


def make_report(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

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
            breakage_info = request.POST.get('breakage_info') if request.POST.get('breakage_info') else ''

            report = Report.objects.create(filled_up=filled_up, date=date, motohour=motohour, fuel=fuel, machine=machine, breakage=breakage)
            
            if breakage:
                machine.breakage = True
                machine.breakage_info = breakage_info
                machine.breakage_date = report.date
                machine.save()

        return redirect('driver:home-page')

    return render(request, 'senior-driver/make_report.html', context)


def show_my_reports(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
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




######### TESTING #########
def make_report_2(request):
    
    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end

    if not request.user.is_superuser:
        can_use_machines = Machine.objects.filter(
            brigade=request.user.seniordriver).exclude(breakage=True)
    else:
        can_use_machines = Machine.objects.all()[:5]

    for obj in can_use_machines:
        obj.el = False

    if request.method == "POST":
        
        date = request.POST.get('date')
        pass_btn_select = False

        # when passed selectMahines submit_button
        if 'selectMachines' in request.POST:
            print('BUTTON SELECT MACHINES CLICKED')
            
            machine_id_list = list(map(lambda el: int(el), request.POST.getlist('choices')))
            machine_list = Machine.objects.filter(id__in=machine_id_list)
            
            for machine in can_use_machines:
                    if machine.id in machine_id_list:
                        machine.el = True

            print(machine_list)
            print(len(machine_list))
            
            context = {
                'selected_machine_bool': True,
                'date_today': date,
                'can_use_machines': can_use_machines,
                'selected_machine_list': machine_list, 
            }
            return render(request, 'senior-driver/test_make_report.html', context)

        # when passed sendData submit_button
        if 'sendData' in request.POST:
            print('BUTTON SEND DATA CLICKED')

            

            machine_id_list = list(map(lambda el: int(el), request.POST.getlist('choices')))
            machine_list = Machine.objects.filter(id__in=machine_id_list)
            
            for machine in can_use_machines:
                    if machine.id in machine_id_list:
                        machine.el = True


            machine_fuel_list = list(map(lambda el: float(el), request.POST.getlist('fuel')))
            machine_motohour_list = list(map(lambda el: int(el), request.POST.getlist('motohour')))
            machine_breakage_list = request.POST.getlist('breakage')
            machine_breakage_info_list = request.POST.getlist('breakage_info')

            for i in range(len(machine_breakage_list)):
                if machine_breakage_list[i] == 'on':
                    machine_breakage_list[i-1] = "del"
            machine_breakage_list = list(filter(lambda el: el == 'on' or el == 'off', machine_breakage_list))
            date = request.POST.get('date')

            
            print("Дата: ", date)
            print("Список машин: ", machine_list)
            print("Список мотогодин: ", machine_motohour_list)
            print("Список бензин: ", machine_fuel_list)
            print("Список поломки: ", machine_breakage_list)
            print("Список информации о поломках: ", machine_breakage_info_list)
            
    
            # создать отчеты
            if not request.user.is_superuser:
                filled_up = request.user.seniordriver
                date = request.POST.get('date')

                report = Report.objects.create(
                    filled_up=filled_up, 
                    date=date, 
                    
                    # потом удалить 
                    motohour=32, 
                    fuel=32, 
                    machine=machine_list[0], 
                    breakage=False)
                
                all_info = list(zip(machine_list, machine_motohour_list, machine_fuel_list, machine_breakage_list, machine_breakage_info_list))
                for el in all_info:
                    
                    breakage = False
                    if el[3] == 'on':
                        breakage = True
                        machine = Machine.objects.get(pk=el[0].id)
                        machine.breakage = breakage
                        machine.breakage_info = el[4]
                        machine.breakage_date = date
                        machine.save()


                    MachineReport.objects.create(
                        report = report,
                        machine = el[0],
                        motohour = el[1],
                        fuel = el[2],
                        breakage = breakage
                    )
                return redirect('driver:home-page')


            context = {
                'selected_machine_bool': True,
                'date_today': date,
                'can_use_machines': can_use_machines,
            }
            return render(request, 'senior-driver/test_make_report.html', context)
        
    context = {
        'can_use_machines': can_use_machines,
        'date_today': datetime.date.today().strftime("%Y-%m-%d")
    }


    return render(request, 'senior-driver/test_make_report.html', context)