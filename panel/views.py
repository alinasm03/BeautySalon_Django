from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
import datetime

import panel.utils
from services.models import Service, Schedule, Master, Booking


@panel.utils.check_admin
def root_handler(request):
    return HttpResponse("Hello panel")


@panel.utils.check_admin
def bookings_handler(request):
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    calendars = Schedule.objects.filter(date__gte=date_start,
                                        date__lte=date_end
                                        ).all()
    available_masters = Master.objects.filter(schedule__in=calendars, status=1).distinct()
    available_services = Service.objects.filter(master__in=available_masters).distinct()
    if request.method == 'POST':
        bookings = Booking(
            master=Master.objects.get(id=request.POST['master']),
            service=Service.objects.get(id=request.POST['service']),
            client=request.POST['client'],
            date=request.POST['datetime'],
            status=True,
        )
        bookings.save()
    bookings = Booking.objects.all()
    pages_booking = Paginator(bookings, 2)
    page_number = request.GET.get('page')
    page_obj = pages_booking.get_page(page_number)
    return render(request, 'panel_bookings.html', {'bookings': bookings,
                                                   'available_masters': available_masters,
                                                   'available_services': available_services,
                                                   'bookings': bookings,
                                                   'page_obj': page_obj
                                                   })


@panel.utils.check_admin
def services_handler(request):
    if request.method == 'POST':
        service = Service(
            name=request.POST['name'],
            duration=request.POST['duration'],
            price=request.POST['price']
        )
        service.save()
    services = Service.objects.all()
    pages_service = Paginator(services, 3)
    page_number = request.GET.get('page')
    page_obj = pages_service.get_page(page_number)
    return render(request, 'panel_service.html', {'services': services,
                                                  'page_obj': page_obj})


@panel.utils.check_admin
def specialist_handler(request):
    if request.method == 'POST':
        specialists = Master(
            name=request.POST['name'],
            range=request.POST['range'],
            phone=request.POST['phone'],
            status=request.POST['status']
         )
        specialists.save()

    service_ids = [value for key, value in request.POST.items() if key.startswith('service')]
    for service_id in service_ids:
        service = Service.objects.get(id=service_id)
        specialists.services.add(service)
    specialists = Master.objects.all().order_by('range')
    services = Service.objects.all()
    pages_master = Paginator(specialists, 1)
    page_number = request.GET.get('page')
    page_obj = pages_master.get_page(page_number)
    return render(request, 'panel_specialists.html',
                  {'specialists': specialists,
                   'services': services,
                   'page_obj': page_obj})


@panel.utils.check_admin
def specialist_id_handler(request, specialist_id):
    if request.method == 'POST':
         work_schedule = Schedule(
            master=Master.objects.get(id=specialist_id),
            date=request.POST['date'],
            time_start=request.POST['time_start'],
            time_end=request.POST['time_end']
         )
         work_schedule.save()
    work_schedule = Schedule.objects.filter(master=specialist_id).all().order_by('date', 'time_start')
    master_actual = Master.objects.filter(id=specialist_id).first()
    pages_schedule = Paginator(work_schedule, 3)
    page_number = request.GET.get('page')
    page_obj = pages_schedule.get_page(page_number)
    return render(request, 'panel_specialist.html', {'specialist': specialist_id,
                                                     'work_schedule': work_schedule,
                                                     'master_actual': master_actual,
                                                     'page_obj': page_obj})


@panel.utils.check_admin
def specialist_schedule(request, specialist_id):
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    available_masters = Master.objects.get(id=specialist_id)
    if request.method == 'POST':
        schedule_master = Schedule(
            master=available_masters,
            date=request.POST['date'],
            time_start=request.POST['time_start'],
            time_end=request.POST['time_end']
        )
        schedule_master.save()
    schedule_master = Schedule.objects.filter(master_id=specialist_id,
                                              date__gte=date_start,
                                              date__lte=date_end)
    pages_schedule = Paginator(schedule_master, 5)
    page_number = request.GET.get('page')
    page_obj = pages_schedule.get_page(page_number)
    return render(request, 'panel_specialist_schedule.html',
                  {'schedule_master': schedule_master,
                   'available_masters': available_masters,
                   'page_obj': page_obj})
