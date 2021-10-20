from django.db    import models

from core.models  import TimeStampModel

class SeatClass(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'seat_classes'

class FlightSchedule(models.Model):
    depature_time = models.DateTimeField()
    arrival_time  = models.DateTimeField()
    airline_code  = models.CharField(max_length=50)

    class Meta:
        db_table = 'flight_schedules'

class Airport(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    class Meta:
        db_table = 'airports'

class AirlinesSchedule(models.Model):
    airport          = models.ForeignKey(Airport, on_delete=models.CASCADE)
    flight_schedule  = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)

    class Meta:
        db_table = 'airlines_schedules'

class Airline(models.Model):
    name       = models.CharField(max_length=50)
    logo_image = models.CharField(max_length=2000)

    class Meta:
        db_table = 'airlines'

class Passenger(TimeStampModel):
    first_name    = models.CharField(max_length=50)
    last_name     = models.CharField(max_length=50)
    nationality   = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender        = models.BooleanField()

    class Meta:
        db_table = "passengers"

class Reservation(models.Model):
    price             = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    departure_date    = models.DateField()
    arrival_date      = models.DateField()
    departure_airport = models.CharField(max_length=50)
    arrival_airport   = models.CharField(max_length=50)
    remain_seat       = models.CharField(max_length=10, null=True)
    airline_change    = models.CharField(max_length=10)
    seat_class        = models.ForeignKey(SeatClass, on_delete=models.SET_NULL, null=True)
    airlines_schedule = models.ForeignKey(AirlinesSchedule, on_delete=models.SET_NULL, null=True)
    airline           = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True)
    passenger         = models.ForeignKey(Passenger, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'reservations'

class AirplaneTaxes(models.Model):
    fuel_surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customs_duty   = models.DecimalField(max_digits=10, decimal_places=2, default=8000)
    ticketing_fee  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reservation    = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'airplane_taxes'