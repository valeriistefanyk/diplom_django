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


def show_my_reports(request):

    # login and permission check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if not ('senior_driver.view_seniordriver' in request.user.get_group_permissions()):
        raise Http404("У Вас не має прав на перегляд цієї сторінки")
    # login and permission check end
    
    my_reports = Report.objects.filter(filled_up__user=request.user)
    
    if request.GET.get('from') and request.GET.get('to'):
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        from_date_correct = correct_date(from_date)
        to_date_correct = correct_date(to_date)
        my_reports = my_reports.filter(date__range = [from_date_correct, to_date_correct])
    else:
        from_date = correct_date(my_reports.earliest('date').date, choise=2)
        to_date = correct_date(my_reports.latest('date').date, choise=2)

    
    my_reports = add_machines(my_reports)

    context = {
        'from_date': from_date,
        'to_date' : to_date,
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


def make_report(request):
    
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
            return render(request, 'senior-driver/make_report.html', context)

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
            return render(request, 'senior-driver/make_report.html', context)
        
    context = {
        'can_use_machines': can_use_machines,
        'date_today': datetime.date.today().strftime("%Y-%m-%d")
    }


    return render(request, 'senior-driver/make_report.html', context)


# ПРАВИЛЬНА ДАТА
def correct_date(date, choise = 1):
    if choise == 1:
        date_list = date.split('/')
        date_correct = f"{date_list[2]}-{date_list[0]}-{date_list[1]}"
        return date_correct
    if choise == 2:
        return date.strftime("%m/%d/%Y")


def add_machines(reports):
    machines_all = Machine.objects.values('id', 'machine__name', 'number_machine', 'inventory_number', 'breakage_info')
    for report in reports:
        machines = []

        for machine in report.machinereport_set.values():
            m = machines_all.get(id=machine['machine_id'])
            machine_full_name =  f"{m['machine__name']} #{m['number_machine']} [IN{m['inventory_number']}] "
            fuel = machine['fuel']
            motohour = machine['motohour']
            breakage = "В ремонті" if machine['breakage'] else "В робочому стані"
            breakage_info = m['breakage_info'] if m['breakage_info'] else 'Інформації про поломку немає'
            
            machines_info = {
                'full_name': machine_full_name,
                'fuel': fuel,
                'motohour': motohour,
                'breakage': breakage,
                'breakage_info': breakage_info
            }
            machines.append(machines_info)
        report.machines = machines
    return reports