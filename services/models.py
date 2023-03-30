from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=60)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Master(models.Model):
    RANGE_CHOICES = (
        (0, 'Майтер'),
        (1, 'Топ-майстер'),
    )
    name = models.CharField(max_length=100)
    range = models.IntegerField(default=0, choices=RANGE_CHOICES)
    phone = models.IntegerField()
    status = models.BooleanField(default=True)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name


class Booking(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.IntegerField()
    date = models.DateTimeField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.master} {self.service} {self.client} {self.date}'


class Schedule(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return f'{self.master} {self.date} {self.time_start} {self.time_end}'
