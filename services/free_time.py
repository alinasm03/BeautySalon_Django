from datetime import timedelta
from services import models


def convert_period_to_set(time_start, time_end):
    time_set = set()
    while time_start <= time_end:
        time_set.add(time_start.replace(tzinfo=None))
        time_start += timedelta(minutes=15)
    return time_set


def calc_free_windows(service, specialist, workday_time_start, workday_time_end):
    free_time = []
    bookings = models.Booking.objects.filter(master=specialist, date__day=workday_time_start.day).all()
    print(bookings)
    busy_time = []
    for booking in bookings:
        booking_time_start = booking.date
        print(booking_time_start)
        booking_time_end = booking.date + timedelta(minutes=booking.service.duration)
        print(booking_time_end)
        busy_time.append(convert_period_to_set(booking_time_start, booking_time_end))
        print(busy_time)
    day_times = sorted(convert_period_to_set(workday_time_start, workday_time_end - timedelta(minutes=service.duration)))
    print('day_times:', day_times)

    for time_start in day_times:
        possible_time = convert_period_to_set(time_start, time_start + timedelta(minutes=service.duration))
        print('time_start:', time_start)
        print('possible_time:', possible_time)
        no_intersection = True
        for one_booking in busy_time:
            print('one_booking:', one_booking)
            print('intersection:', possible_time.intersection(one_booking))
            #one_booking = one_booking.replace(tzinfo=None)
            #print('one_booking:', one_booking)
            if len(possible_time.intersection(one_booking)) > 1:
                print('one_booking:', one_booking)
                no_intersection = False
                break
        if no_intersection:
            #print('free_time:', free_time)
            free_time.append(time_start)
    return free_time
