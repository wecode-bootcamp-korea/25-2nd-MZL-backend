# Generated by Django 3.2.8 on 2021-10-28 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('eng_name', models.CharField(default='', max_length=45)),
                ('logo_url', models.URLField(default='', max_length=1000)),
            ],
            options={
                'db_table': 'airlines',
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('eng_name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'airports',
            },
        ),
        migrations.CreateModel(
            name='Weekday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'weekdays',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=45)),
                ('depart_time', models.TimeField()),
                ('arrive_time', models.TimeField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('remain_seats', models.IntegerField(default=0)),
                ('seat_class', models.CharField(max_length=45)),
                ('flight_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.airline')),
                ('airport_arrive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrive', to='reservations.airport')),
                ('airport_depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depart', to='reservations.airport')),
            ],
            options={
                'db_table': 'reservations',
            },
        ),
        migrations.CreateModel(
            name='FlightWeekday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weekday', models.CharField(max_length=45)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.reservation')),
            ],
            options={
                'db_table': 'flight_weekdays',
            },
        ),
        migrations.CreateModel(
            name='AirplaneTaxes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_surcharge', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('customs_duty', models.DecimalField(decimal_places=2, default=8000, max_digits=10)),
                ('ticketing_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('reservation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.reservation')),
            ],
            options={
                'db_table': 'airplane_taxes',
            },
        ),
    ]
