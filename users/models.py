from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    name          = models.CharField(max_length=50)
    email         = models.CharField(max_length=200, null=True)
    kakao_id      = models.CharField(max_length=200)
    point         = models.DecimalField(max_digits=10, decimal_places=2, default=4560000)
    
    class Meta:
        db_table = "users"