from django.urls            import path

from reservations.models    import AirplaneTaxes, Reservation
from reservations.views     import ReservationView

urlpatterns = [
    path('', ReservationView.as_view()),
]