import json
import random
import datetime

from django.db.models import Q 
from django.views     import View
from django.http      import JsonResponse, HttpResponse

from .models          import AirplaneTaxes, Reservation, FlightWeekday


class ReservationView(View):
    def get(self, request):
        departure           = request.GET.get("departure", None)   
        arrival             = request.GET.get("arrival", None)    
        airport_depart_name = request.GET.get("airport_depart", None)   
        airport_arrive_name = request.GET.get("airport_arrive", None)   
        start_date          = request.GET.get("start_date", None)   
        end_date            = request.GET.get("end_date", None)   
        airline_list        = request.GET.getlist('airline_list', None)   
        seat_class          = request.GET.getlist('seat_class', None)   

        q = Q()
        if airline_list:
            q &= Q(airline__name__in = airline_list)
        if seat_class:
            q &= Q(seat_class__in = seat_class)

        if departure:
            flight_condition = {
                'depart_date' : start_date,
                'depart'      : airport_depart_name,
                'arrive'      : airport_arrive_name
            }
        elif arrival:
            flight_condition = {
                'depart_date' : end_date,
                'depart'      : airport_arrive_name,
                'arrive'      : airport_depart_name
            }
        else:
            return JsonResponse({"message":"Not Found URL"}, status=400)

        reservations = Reservation.objects.select_related(
            "airline","airport_depart","airport_arrive").prefetch_related(
                "flightweekday_set").filter(
                    airport_depart__name = flight_condition['depart'],
                    airport_arrive__name = flight_condition['arrive'], 
                    flightweekday__date = flight_condition['depart_date']
                    ).filter(q)

        reservation_list = [{
            "id"                 : reservation.id,
            "airport_depart"     : flight_condition['depart'],
            "airport_arrive"     : flight_condition['arrive'],
            "depart_date"        : flight_condition['depart_date'],
            "depart_weekday"     : FlightWeekday.objects.filter(date = flight_condition['depart_date'], reservation_id = reservation.id).first(0).weekday,
            "flightcode"         : reservation.flightcode,
            "airport_depart_eng" : reservation.airport_depart.eng_name,                    
            "airport_arrive_eng" : reservation.airport_arrive.eng_name,
            "depart_time"        : reservation.depart_time,
            "arrive_time"        : reservation.arrive_time,
            "airline"            : reservation.airline.name,
            "airline_url"        : reservation.airline.logo_url,
            "remain_seats"       : reservation.remain_seats,
            "flight_price"       : reservation.flight_price,
            "seat_class"         : reservation.seat_class
        } for reservation in reservations]
        low_price = Reservation.objects.order_by(reservation_list,'flight_price')
        return JsonResponse({"message":"SUCCESS!", "flight_list":low_price}, status=200)

class AirplaneTaxeView(View):  
    def get(self, request):
        fuel_surcharge = request.GET.get('fuel_surcharge')
        customs_duty   = request.GET.get('customs_duty')
        ticketing_fee  = request.GET.get('ticketing_fee')
        total_price    = AirplaneTaxes.aggregate(total_price=('price'))

        return JsonResponse({
            'fuel_surcharge' : fuel_surcharge,
            'customs_duty'   : customs_duty,
            'ticketing_fee'  : ticketing_fee,
            'total_price'    : total_price,},
             status = 200)