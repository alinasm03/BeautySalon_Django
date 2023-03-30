import datetime
from django.shortcuts import render
from django.http import HttpResponse
from services.models import Service, Master, Schedule


def service_handler(request):
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    # day_of_week = date_start.weekday()
    # monday = date_start - datetime.timedelta(days=day_of_week)
    # sunday = date_start + datetime.timedelta(days=6 - day_of_week)
    # week = f'{monday} -- {sunday}'
    week = f'{date_start} -- {date_end}'

    calendars = Schedule.objects.filter(date__gte=date_start,
                                        date__lte=date_end
                                        ).all()
    available_masters = Master.objects.filter(schedule__in=calendars, status=1).distinct()
    services = Service.objects.filter(master__in=available_masters).distinct()
    return render(request, 'service.html', {'services': list(services), 'week': week})


def service_name_handler(request, service_name):
    return HttpResponse(f"Service - {service_name}")


def specialist_handler(request):
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    #day_of_week = date_start.weekday()
    #monday = date_start - datetime.timedelta(days=day_of_week)
    #sunday = date_start + datetime.timedelta(days=6 - day_of_week)
    #week = f'{monday} -- {sunday}'
    week = f'{date_start} -- {date_end}'

    calendars = Schedule.objects.filter(date__gte=date_start,
                                        date__lte=date_end
                                        ).all()
    available_masters = Master.objects.filter(schedule__in=calendars, status=1).distinct()
    return render(request, 'specialist.html', {'specialists': list(available_masters), 'week': week})


def specialist_id_handler(request, specialist_id):
    return HttpResponse(f"Hello specialist, {specialist_id}")


def booking_handler(request):
    return HttpResponse("Booking")
