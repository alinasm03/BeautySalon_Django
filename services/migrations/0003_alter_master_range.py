# Generated by Django 4.1.7 on 2023-05-08 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_alter_schedule_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='range',
            field=models.IntegerField(choices=[(0, 'Майcтер'), (1, 'Топ-майстер')], default=0),
        ),
    ]
