import datetime
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test import Client
from services.models import Service, Master, Booking, Schedule


class TestBooking(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='admin1', password='1234')
        user.save()
        group = Group.objects.create(name='salon_admin_panel')
        group.save()
        user.groups.add(group)
        user.save()

    def test_booking(self):
        c = Client()
        c.login(username='admin1', password='1234')
        service_1 = Service.objects.create(name="test_serv_1", duration=60, price=1000)
        service_1.save()
        specialist = Master.objects.create(name="User_test", range=1, phone=997892233, status=True)
        specialist.services.add(service_1)
        specialist.save()
        response = c.post("/panel/bookings/",
                          {"master": f"{specialist.id}",
                           "service": f"{service_1.id}",
                           "client": 1,
                           "datetime": '2023-05-15 12:00',
                           "status": True
                           })
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(master=specialist, service=service_1)
        self.assertEqual(booking.date, datetime.datetime(2023, 5, 15, 12, 0, tzinfo=datetime.timezone.utc))


class Test(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='admin1', password='1234')
        user.save()
        group = Group.objects.create(name='salon_admin_panel')
        group.save()
        user.groups.add(group)
        user.save()

    def test_panel_specialist(self):
        c = Client()
        c.login(username='admin1', password='1234')
        sev1 = Service(name="test1", duration=1, price=1)
        sev1.save()
        service_db = Service.objects.all()
        self.assertEqual(len(service_db), 1)
        response = c.post("/panel/specialist/", {"name": "Alina", "range": "1",
                                                 "phone": "0500571106", "status": "1",
                                                 f"service_{sev1.id}": f"{sev1.id}"})

        self.assertEqual(response.status_code, 200)
        specialist = Master.objects.filter(name="Alina")
        self.assertEqual(len(specialist), 1)

    def test_panel_services(self):
        c = Client()
        c.login(username='admin1', password='1234')
        response = c.post("/panel/services/", {"name": "test1", "duration": "1", "price": "10"})
        self.assertEquals(response.status_code, 200)
        all_services = Service.objects.filter(name="test1")
        self.assertEquals(len(all_services), 1)

    def test_panel_schedule(self):
        c = Client()
        c.login(username='admin1', password='1234')
        service = Service(name="test_calendar", duration=1, price=1)
        service.save()
        specialist = Master(name="Alina", range=1, phone=997892233, status=True)
        specialist.save()
        specialist.services.add(service)
        specialist.save()
        response = c.post(f"/panel/specialist/{specialist.id}/schedule/",
                          {"master": f"{specialist.id}", "date": '2023-05-11',
                           "time_start": '12:00:00', "time_end": '18:00:00'
                           })
        self.assertEqual(response.status_code, 200)
        calendar = Schedule.objects.filter(master=specialist)
        self.assertEqual(len(calendar), 1)
