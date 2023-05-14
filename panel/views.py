from django.shortcuts import render
from django.http import HttpResponse
import datetime
from services.models import Service, Schedule, Master, Booking


def root_handler(request):
    if not request.user.groups.filter(name='salon_admin_panel'):
        return HttpResponse('Немає доступу до перегляду сторінки')
    return HttpResponse("Hello panel")


def bookings_handler(request):
    if not request.user.groups.filter(name='salon_admin_panel'):
        return HttpResponse('Немає доступу до перегляду сторінки')
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    calendars = Schedule.objects.filter(date__gte=date_start,
                                        date__lte=date_end
                                        ).all()
    available_masters = Master.objects.filter(schedule__in=calendars, status=1).distinct()
    available_services = Service.objects.filter(master__in=available_masters).distinct()
    if request.method == 'POST':
        #master = Master.objects.get(id=request.POST['master'])
        #service = Service.objects.get(id=request.POST['service'])
        bookings = Booking(
            master=Master.objects.get(id=request.POST['master']),
            service=Service.objects.get(id=request.POST['service']),
            client=request.POST['client'],
            date=request.POST['datetime'],
            status=True,
        )
        bookings.save()
    bookings = Booking.objects.all()
    return render(request, 'panel_bookings.html', {'bookings': bookings,
                                                   'available_masters': available_masters,
                                                   'available_services': available_services,
                                                   'bookings': bookings
                                                   })


def services_handler(request):
    if not request.user.groups.filter(name='salon_admin_panel'):
        return HttpResponse('Немає доступу до перегляду сторінки')
    if request.method == 'POST':
        service = Service(
            name=request.POST['name'],
            duration=request.POST['duration'],
            price=request.POST['price']
        )
        service.save()
    services = Service.objects.all()
    return render(request, 'panel_service.html', {'services': services})


def specialist_handler(request):
    if not request.user.groups.filter(name='salon_admin_panel'):
        return HttpResponse('Немає доступу до перегляду сторінки')
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
    return render(request, 'panel_specialists.html',
                  {'specialists': specialists, 'services': services})


def specialist_id_handler(request, specialist_id):
    if not request.user.groups.filter(name='salon_admin_panel'):
        return HttpResponse('Немає доступу до перегляду сторінки')
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
    return render(request, 'panel_specialist.html', {'specialist': specialist_id,
                                                     'work_schedule': work_schedule,
                                                     'master_actual': master_actual})


def specialist_schedule(request, specialist_id):
    if not request.user.groups.filter(name='salon_admin_panel'):
        return HttpResponse('Немає доступу до перегляду сторінки')
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
    return render(request, 'panel_specialist_schedule.html',
                  {'schedule_master': schedule_master,
                   'available_masters': available_masters})
