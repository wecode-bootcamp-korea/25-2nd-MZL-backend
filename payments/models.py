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