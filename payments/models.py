from django.db           import models

from core.models         import TimeStampModel
from reservations.models import Reservation
from users.models        import User

class PayMent(TimeStampModel):
    total_price = models.DecimalField(max_digits=15, decimal_places=3)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "payments"

class Passenger(TimeStampModel):
    first_name    = models.CharField(max_length=50)
    last_name     = models.CharField(max_length=50)
    nationality   = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender        = models.BooleanField()

    class Meta:
        db_table = "passengers"