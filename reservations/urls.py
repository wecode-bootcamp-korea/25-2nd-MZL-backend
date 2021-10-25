from django.urls            import path

from reservations.models    import Reservation
from reservations.views     import ReservationView

urlpatterns = [
    path('', ReservationView.as_view()),
]