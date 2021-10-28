import json
import random
import datetime

from django.db.models import Q 
from django.views     import View
from django.http      import JsonResponse, HttpResponse

from reservations.models          import Airline, AirplaneTaxes, Airport, Reservation


class ReservationView(View):
    def get(self, request): 
        date           = request.GET.get("start_date", None)      
        airline_list   = request.GET.getlist('airline_list', None)   
        seat_class     = request.GET.get('seat_class', None)
        time_option    = request.GET.get('time_option', None)
        airport_depart = request.GET.getlist('airport_depart', None)

        sort_option = {
            'departureTime:asc'  : 'departure_time',
            'departureTime:desc' : '-departure_time',
            'price:asc'          : 'fligt_prices_price'
        }
        q = Q()

        if date:
            q &= Q(start_date=date)

        if seat_class:
            q &= Q(seat_class=seat_class)

        if airline_list:
            q &= Q(airline__name__in=airline_list)

        if time_option == 'am':
            q &= Q(depart_time__lt = '12:00:00')

        if time_option == 'pm':
            q &= Q(depart_time__gte = '12:00:00')

        if airport_depart:
            q &= Q(airport_depart__name__in=airport_depart)

        reservations = Reservation.objects.filter(q).select_related(
            'airport_depart','airport_arrive','airline').order_by(sort_option.get('sort','flight_price'))

        reservation_list = [{
            "id"                 : reservation.id,
            "airport_depart"     : reservation.airport_depart.name,
            "airport_arrive"     : reservation.airport_arrive.name,
            "start_date"         : reservation.start_date,
            "end_date"           : reservation.end_date,
            "flight_code"        : reservation.flight_code,
            "airport_depart_eng" : reservation.airport_depart.eng_name,                    
            "airport_arrive_eng" : reservation.airport_arrive.eng_name,
            "depart_time"        : reservation.depart_time,
            "arrive_time"        : reservation.arrive_time,
            "airline"            : reservation.airline.name,
            "airline_logo"       : reservation.airline.logo_url,
            "remain_seats"       : reservation.remain_seats,
            "flight_price"       : reservation.flight_price,
            "seat_class"         : reservation.seat_class,
        } for reservation in reservations]

        return JsonResponse({"data": reservation_list}, status=200)
