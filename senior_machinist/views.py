from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Sum
from django.conf import settings

from machines.models import Machine
from engineer.models import Report, MachineReport, Engineer
from director.models import Director
from senior_machinist.models import SeniorMachinist, BrigadeMembers
from senior_machinist.models import TempReport, BrigadeInfoReport, MachineWorkingReport, MasloInfoReport, MotoAndFuelInfoReport
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.core.files.storage import FileSystemStorage
from PIL import Image
from io import BytesIO


@login_required
@permission_required('senior_machinist.full_control', raise_exception=True)
def home_page(request):
    """ Початкова сторінка старшого машиніста """

    return render(request, 'senior-machinist/home_page.html', context={})


@login_required
@permission_required('senior_machinist.full_control', raise_exception=True)
def my_machine(request):
    """ Машина яка закріплена за старшим машиністом """

    machinist = set_machinist(request.user)

    # machine = get_object_or_404(Machine, machine=machinist.machine)
    context = {
        'machine': machinist.machine,
    }
    return render(request, 'senior-machinist/my_machine.html', context)


@login_required
@permission_required('senior_machinist.full_control', raise_exception=True)
def management_contact(request):
    
    machinist = set_machinist(request.user)

    engineers = Engineer.objects.all().select_related('user')
    directors = Director.objects.all().select_related('user')
    context = {
        'machinist': machinist,
        'engineers': engineers,
        'directors': directors,
    }

    if request.method == 'POST' and request.FILES['avatar']:
        avatar = request.FILES['avatar']
        fs = FileSystemStorage()

        limit = 10* 1024 * 1024
        if not avatar.name.endswith(('.jpg', '.png', '.jpeg')):
            context['msg'] = 'Формат фотографії повинен бути .jpg, .jpeg або .png'
            return render(request, 'senior-machinist/contacts_page.html', context)
        if avatar.size > limit:
            context['msg'] = 'Розмір фотографії перевищує 10МБ. Завантажте фото менше за розміром'
            return render(request, 'senior-machinist/contacts_page.html', context)
        
        im = Image.open(avatar)
        im_io = BytesIO() 
        im.save(im_io, 'JPEG', quality=60)

        filename = fs.save('employees/' + avatar.name, im_io)
        uploaded_file_url = fs.url(filename)
        machinist.avatar = 'employees/' + avatar.name
        machinist.save()

    return render(request, 'senior-machinist/contacts_page.html', context)


@login_required
@permission_required('senior_machinist.full_control', raise_exception=True)
def brigade_members(request):
    
    machinist = set_machinist(request.user)
    members = BrigadeMembers.objects.filter(seniormachinist=machinist)
    context = {
        'members': members,
    }
    return render(request, 'senior-machinist/brigade_members.html', context)


def route_sheet(request):

    STAGE = {
        'prepare': 'prepare',
        'full': 'full',
        'part': 'part',
        'prefull': 'prefull',
        'prepart': 'prepart',
    }

    machinist = set_machinist(request.user)
    members = BrigadeMembers.objects.filter(seniormachinist=machinist)
    
    date = request.POST.getlist('date')[0] if request.POST.getlist('date') else None
    context = {
            'members': members,
            'stage': STAGE['prepare'],
        }

    
    

    if request.POST.get('sendDataFirst'):
        date = request.POST.getlist('date')[0] if request.POST.getlist('date') else None
        members_id_list = list(map(lambda el: int(el), request.POST.getlist('choices')))
        members = members.filter(id__in=members_id_list)
        try:
            temp_report = TempReport.objects.create(
                filled_up = machinist,
                date = date,
                stage = 'strt',
                machine = machinist.machine,
            )
        except IntegrityError:
            temp_report = TempReport.objects.get(date=date)
            context["msg"] = "Такой отчет уже существует"
        

        print('temp_report: ', temp_report)

        context['date'] = date
        context['temp_report'] = temp_report
        context['members'] = members
        context['stage'] = STAGE['full']
    
    if request.POST.get('sendDataBrigade'):
        date = request.POST.getlist('date')[0] if request.POST.getlist('date') else None
        members_id_list = list(map(lambda el: int(el), request.POST.getlist('member_id')))
        date_time_from_list = request.POST.getlist('date_time_from')
        date_time_to_list = request.POST.getlist('date_time_to')
        medical_check_before_list = request.POST.getlist('medical_check_before')
        medical_check_after_list = request.POST.getlist('medical_check_after')
        
        members = members.filter(id__in=members_id_list)
        temp_report = TempReport.objects.get(date=date)
        temp_report.stage = 'part'
        temp_report.save()

        brigade_info_report = []
        for i in range(len(members)):
            temp = BrigadeInfoReport.objects.create(
                member = members[i],
                report = temp_report,
                
                medical_check_before = medical_check_before_list[i],
                medical_check_after = medical_check_after_list[i]
            )

            if date_time_from_list[i]:
                temp.date_time_from = f"{date} {date_time_from_list[i]}"
            if date_time_to_list[i]:
                temp.date_time_to = f"{date} {date_time_to_list[i]}"
            temp.save()
            brigade_info_report.append(temp)

        print(brigade_info_report)
        context['date'] = date
        context['temp_report'] = temp_report
        context['members'] = members

        # temp
        context['stage'] = STAGE["full"]

    # заповнення мотогодини і використане паливо
    if request.POST.get('sendDataMotoFuel'):
        date = request.POST.getlist('date')[0] if request.POST.getlist('date') else None
        km_before = request.POST.get('km_before')
        motohour_before = request.POST.get('motohour_before')
        km_after = request.POST.get('km_after')
        motohour_after = request.POST.get('motohour_after')
        
        temp_report = TempReport.objects.get(date=date)
        try:
            motoandfuelinfo = MotoAndFuelInfoReport.objects.create(
                report = temp_report,
            )
            if km_before:
                motoandfuelinfo.km_before = km_before
            if km_after:
                motoandfuelinfo.km_after = km_after
            if motohour_before:
                motoandfuelinfo.motohour_before = motohour_before
            if motohour_after:   
                motoandfuelinfo.motohour_after = motohour_after
            motoandfuelinfo.save()

            if km_after and km_before:
                temp_report.km = float(km_after) - float(km_before)
            if motohour_after and motohour_before:
                temp_report.motohour = int(motohour_after) - int(motohour_before)
            
            temp_report.stage = 'part'
            temp_report.save()

        except IntegrityError:
            context['msg'] = 'такі дані вже існують'
        

        print(date, km_before, motohour_before, km_after, motohour_after, temp_report)

        members_id_list = list(map(lambda el: int(el), request.POST.getlist('member_id')))
        members = members.filter(id__in=members_id_list)

        context['date'] = date
        context['temp_report'] = temp_report

        context['members'] = members
        # temp
        context['stage'] = STAGE["full"]


    # заповнення масла
    if request.POST.get('sendDataMasloInfo'):
        date = request.POST.getlist('date')[0] if request.POST.getlist('date') else None
        marka = request.POST.get('marka')
        vidano = request.POST.get('vidano')
        maslo_before = request.POST.get('maslo_before')
        maslo_after = request.POST.get('maslo_after')
        info = request.POST.get('info')
        
        temp_report = TempReport.objects.get(date=date)
        try:
            masloinforeport = MasloInfoReport.objects.create(
                report = temp_report,
                marka = marka,
                vidano = vidano,  
                info = info,
            )

            if maslo_before:
                masloinforeport.maslo_before = maslo_before
            if maslo_after:
                masloinforeport.maslo_after = maslo_after
            masloinforeport.save()

            if maslo_after and maslo_before:
                temp_report.maslo = float(maslo_after) - float(maslo_before)
            temp_report.stage = 'part'
            temp_report.save()

        except IntegrityError:
            context['msg'] = 'такі дані вже існують'

        


        members_id_list = list(map(lambda el: int(el), request.POST.getlist('member_id')))
        members = members.filter(id__in=members_id_list)
        context['members'] = members

        context['date'] = date
        context['temp_report'] = temp_report

        # temp
        context['stage'] = STAGE["full"]

    
    # заповнення інформацію про машини
    if request.POST.get('sendDataMachineWorking'):
        date = request.POST.getlist('date')[0] if request.POST.getlist('date') else None
        client = request.POST.get('client')
        station_from = request.POST.get('station_from')
        station_to = request.POST.get('station_to')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        description = request.POST.get('description')
        place_working = request.POST.get('place_working')
        workday_production = request.POST.get('workday_production')
        
        temp_report = TempReport.objects.get(date=date)
        
        temp_report.stage = 'part'
        temp_report.save()

        temp_mw = MachineWorkingReport.objects.create(
            report = temp_report,
            client = client,
            station_from = station_from, 
            station_to = station_to,
            description = description,
            place_working = place_working, 
            workday_production = workday_production,
        )
        if departure_time:
            temp_mw.departure_time = f"{date} {departure_time}"
        if arrival_time:
            temp_mw.arrival_time = f"{date} {arrival_time}"
        
        members_id_list = list(map(lambda el: int(el), request.POST.getlist('member_id')))
        members = members.filter(id__in=members_id_list)
        context['members'] = members

        context['date'] = date
        context['temp_report'] = temp_report

        # temp
        context['stage'] = STAGE["full"]

    if request.session.get('_old_post'):
        old_post = request.session.get('_old_post')
        date = old_post['date']
        temp_report_id = old_post['temp_report_id']
        member_id_list = old_post['member_id']

        request.session.pop('_old_post')
        
        member_id_list = list(map(lambda el: int(el), eval(member_id_list)))
        members = members.filter(id__in=member_id_list)
        
        temp_report = get_object_or_404(TempReport, pk=temp_report_id)
        temp_report.stage = 'part'
        temp_report.save()

        context['stage'] = STAGE["full"]
        context['date'] = date
        context['members'] = members
        context['temp_report'] = temp_report


    if request.POST.get('mydate'):
        mydate = request.POST.get('mydate')
        
        temp_report = TempReport.objects.get(date=mydate)
        brigadeinforeport = temp_report.brigadeinforeport_set.values_list('member_id', flat=True)
        if brigadeinforeport:
            members = members.filter(id__in=brigadeinforeport)

            context['date'] = mydate
            context['members'] = members
            context['stage'] = STAGE['full']
            context['temp_report'] = temp_report
    
        context['mydate'] = mydate
        date = mydate

    if date:
        print('есть дата!')
        temp_report = TempReport.objects.get(date=date)
        context['temp_report'] = temp_report

        if BrigadeInfoReport.objects.filter(report = temp_report).exists():
            context['exist_brigade_info_report'] = True
        if MachineWorkingReport.objects.filter(report = temp_report).exists():
            context['exist_machine_working_report'] = True
        if MasloInfoReport.objects.filter(report = temp_report).exists():
            context['exist_maslo_info_report'] = True
        if MotoAndFuelInfoReport.objects.filter(report = temp_report).exists():
            context['exist_moto_fuel_info_report'] = True

    

    return render(request, 'senior-machinist/route_sheet_create.html', context)


@login_required
@permission_required('senior_machinist.full_control', raise_exception=True)
def machine_working_fill(request):
    """ Заповнення інформації про машини """

    machinist = set_machinist(request.user)
    route_sheets = TempReport.objects.filter(filled_up=machinist)

    context = {
        'google_api_key': settings.GOOGLE_MAPS_API_KEY,
    }

    if request.POST.get('msg'):
        context['temp_report_id'] = request.POST['temp_report_id']
        context['date'] = request.POST['date']
        context['member_id'] = request.POST.getlist('member_id')

    if request.POST.get('sendDataMachineWorking'):

        create_machine_working_report(request)

        context['temp_report_id'] = request.POST['temp_report_id']
        context['date'] = request.POST['date']
        context['member_id'] = request.POST.get('member_id')

        request.session['_old_post'] = request.POST
        return redirect('machinist:route-sheet')
        

    if request.POST.get('sendDataAddMachine'):
        
        create_machine_working_report(request)

        context['temp_report_id'] = request.POST['temp_report_id']
        context['date'] = request.POST['date']
        context['member_id'] = request.POST.get('member_id')

    
    
    return render(request, 'senior-machinist/_machine_working_fill.html', context)


@login_required
@permission_required('senior_machinist.full_control', raise_exception=True)
def show_route_sheet(request):
    """ Створені марщрутні листи """

    machinist = set_machinist(request.user)
    route_sheets = TempReport.objects.filter(filled_up=machinist).order_by('-date')

    context = {}

    if request.POST.get('sendDataFinish'):
        temp_report_id = request.POST['temp_report']
        
        temp_report = TempReport.objects.get(id=temp_report_id)
        temp_report.stage = 'fwdi'
        temp_report.save()
        date = request.POST.get('date')
        if date:
            context['msg'] = f'Маршрутний лист за {date} створений та переданий інженеру. Лист має №{temp_report_id}<br>Подивитись вміст можете на цій сторінці.'
        else:
            context['msg'] = f'Маршрутний лист №{temp_report_id} був переданий інженеру.'

    if request.POST.get('sendDeleteReady'):
        temp_report_id = request.POST.get('temp_report_id')
        temp_report = route_sheets.get(id=temp_report_id)
        temp_report.delete()

        context['msg'] = f'Маршрутний лист №{temp_report_id} успішно видалений'
        
    context['forward_route_sheets'] = route_sheets.exclude(stage__in=['strt', 'part', 'no'])
    context['start_route_sheets'] = route_sheets.filter(stage='strt')
    context['part_route_sheets'] = route_sheets.filter(stage='part')
    
    return render(request, 'senior-machinist/route_sheet_show.html', context)


@login_required
@permission_required('senior_machinist.full_control', raise_exception=True)
def route_sheet_detail(request, route_sheet_id):
    """ Детально про маршрутний лист """

    machinist = set_machinist(request.user)
    route_sheet_detail = get_object_or_404(TempReport, pk=route_sheet_id)

    brigade_info_reports = BrigadeInfoReport.objects.filter(report = route_sheet_detail)
    machine_working_reports = MachineWorkingReport.objects.filter(report = route_sheet_detail)
    try:
        maslo_info_report = MasloInfoReport.objects.get(report = route_sheet_detail)
    except ObjectDoesNotExist:
        maslo_info_report = None
    try:
        moto_fuel_info_report = MotoAndFuelInfoReport.objects.get(report = route_sheet_detail)
    except ObjectDoesNotExist:
        moto_fuel_info_report = None

    data_for_js = []
    for machinereport in machine_working_reports:

        if machinereport.latFld and machinereport.lngFld:
            data = [machinereport.description, machinereport.latFld, machinereport.lngFld]
            data_for_js.append(data)
    
    
    if len(data_for_js) > 1:
        lat_arr = [el[1] for el in data_for_js]
        lng_arr = [el[2] for el in data_for_js]
        center_lat = sum(lat_arr)/len(lat_arr)
        center_lng = sum(lng_arr)/len(lng_arr)
        center = {"lat": center_lat, "lng": center_lng}
    elif len(data_for_js) == 1:
        center = {"lat": data_for_js[0][1], "lng": data_for_js[0][2]}
    else:
        center = {"lat": 50.443165, "lng": 30.485434}

    context = {
        'route_sheet': route_sheet_detail,
        'brigade_info_reports': brigade_info_reports,
        'maslo_info_report': maslo_info_report,
        'moto_fuel_info_report': moto_fuel_info_report,
        'machine_working_reports': machine_working_reports,

        'data_for_js': data_for_js,
        'center_map': center,
        'google_api_key': settings.GOOGLE_MAPS_API_KEY,
    }

    return render(request, 'senior-machinist/route_sheet_detail.html', context)


@login_required
@permission_required('senior_machinist.full_control', raise_exception=True)
def machine_status(request):
    """ Інформація про стан машини """

    machinist = set_machinist(request.user)

    machine = machinist.machine


    if request.POST.get('sendBreakageInfo'):
        

        breakage_info = request.POST.get('breakage_info')
        breakage_date = request.POST.get('breakage_date')
        status = request.POST.get('status')

        machine.breakage = True
        machine.fix_by = f"{machinist.user.last_name} {machinist.user.first_name[0]}"
        machine.machine_condition = '2'

        if breakage_info:
            machine.breakage_info = breakage_info
        if breakage_date:
            machine.breakage_date = breakage_date
        if status:
            machine.status = status
            if status == '2':
                machine.machine_condition = '1'
        else:
            machine.status = '5'
        
        machine.save()
        
    if request.POST.get('sendFixInfo'):

        fix_date = request.POST.get('fix_date')
        status_condition = request.POST.get('status_condition')

        machine.breakage = False
        machine.fix_by = f"{machinist.user.last_name} {machinist.user.first_name[0]}"
        machine.status = '0'
        machine.machine_condition = '0'
        if fix_date:
            machine.fix_date = fix_date
        machine.save()

    context = {
        'machine': machine
    }
    return render(request, 'senior-machinist/machine_status.html', context)


#### ДОПОМІЖНІ МЕТОДИ ####
def set_machinist(user):
    if user.is_superuser:
        return SeniorMachinist.objects.all().select_related('user')[1]
    return user.seniormachinist


def create_machine_working_report(request):

    date = request.POST['date']
    temp_report_id = request.POST['temp_report_id']
    temp_report = get_object_or_404(TempReport, pk=temp_report_id)
    latFld = request.POST['latFld']
    lngFld = request.POST['lngFld']
    workday_production = request.POST['workday_production']
    description = request.POST['description']
    client = request.POST['client']
    station_from = request.POST['station_from']
    station_to = request.POST['station_to']
    departure_time = request.POST['departure_time']
    arrival_time = request.POST['arrival_time']

    machine_working_report = MachineWorkingReport.objects.create(
        report = temp_report,
    )
    if latFld and lngFld:
        machine_working_report.latFld = latFld
        machine_working_report.lngFld = lngFld
    if workday_production:
        machine_working_report.workday_production = workday_production
    if description:
        machine_working_report.description = description
    if client: 
        machine_working_report.client = client
    if station_from: 
        machine_working_report.station_from = station_from
    if station_to: 
        machine_working_report.station_to = station_to
    if departure_time:
            machine_working_report.departure_time = f"{date} {departure_time}"
    if arrival_time:
        machine_working_report.arrival_time = f"{date} {arrival_time}"
    machine_working_report.save()