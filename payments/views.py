import json

from datetime            import datetime, date

from django.http         import JsonResponse
from django.views        import View
from django.db           import transaction

from payments.models     import Passenger
from reservations.models import Reservation

from utils               import login_decorator

class PaymentView(View):
    @login_decorator
    @transaction.atomic
    def get(self, request):
        get_depa_air            = request.GET.get('depa-air')
        get_arri_air            = request.GET.get('arri-air')
        depa_air_info           = Reservation.objects.filter(id = get_depa_air).first()
        arri_air_info           = Reservation.objects.filter(id = get_arri_air).first()
        total_price_int         = int(arri_air_info.flight_price) + int(depa_air_info.flight_price)
        outbound_arrival_time   = depa_air_info.arrive_time
        outbound_departure_time = depa_air_info.depart_time
        inbound_arrival_time    = arri_air_info.arrive_time
        inbound_arrival_time    = arri_air_info.depart_time
        depa_flight_duration    = datetime.combine(date.today(), outbound_arrival_time) - datetime.combine(date.today(), outbound_departure_time)
        arri_flight_duration    = datetime.combine(date.today(), inbound_arrival_time) - datetime.combine(date.today(), inbound_arrival_time)
        user                    = request.user

        user_info = {
            "name"  : user.name,
            "email" : user.email
        }
        
        depa_air_info = {
            "departure_airport"       : depa_air_info.airport_depart.name,
            "departure_airport_eng"   : depa_air_info.airport_depart.eng_name,
            "departure_time"          : depa_air_info.depart_time,
            "arrival_airport"         : depa_air_info.airport_arrive.name,
            "arrival_airport_eng"     : depa_air_info.airport_arrive.eng_name,
            "arrival_time"            : depa_air_info.arrive_time,
            "depa_airline_name"       : depa_air_info.airline.name,
            "depa_airline_logo"       : depa_air_info.airline.logo_url,
            "airplane_code"           : depa_air_info.flight_code,
            "seat_class"              : depa_air_info.seat_class,
            "price"                   : int(depa_air_info.flight_price),
            "start_date"              : depa_air_info.start_date,
            "remain_seats"            : depa_air_info.remain_seats,
            "flight_duration"         : str(depa_flight_duration),  
        }

        arri_air_info = {
            "departure_airport"       : arri_air_info.airport_depart.name,
            "departure_airport_eng"   : arri_air_info.airport_depart.eng_name,
            "departure_time"          : arri_air_info.depart_time,
            "arrival_airport"         : arri_air_info.airport_arrive.name,
            "arrival_airport_eng"     : arri_air_info.airport_arrive.eng_name,
            "arrival_time"            : arri_air_info.arrive_time,
            "depa_airline_name"       : arri_air_info.airline.name,
            "depa_airline_logo"       : arri_air_info.airline.logo_url,
            "airplane_code"           : arri_air_info.flight_code,
            "seat_class"              : arri_air_info.seat_class,
            "price"                   : int(arri_air_info.flight_price),
            "start_date"              : arri_air_info.start_date,
            "remain_seats"            : arri_air_info.remain_seats,
            "flight_duration"         : str(arri_flight_duration),  
        }

        total_price = {
            "total_price" : total_price_int
        }
        
        return JsonResponse({"user_info": user_info, "depature_airplane_info" : depa_air_info, "arrival_airplane_info" : arri_air_info, "total_price" : total_price })

    @login_decorator
    @transaction.atomic
    def post(self, request):
        data            = json.loads(request.body)
        user            = request.user
        get_depa_air    = request.GET.get('depa-air')
        get_arri_air    = request.GET.get('arri-air')
        depa_air_info   = Reservation.objects.filter(id = get_depa_air).first()
        arri_air_info   = Reservation.objects.filter(id = get_arri_air).first()
        total_price_int = int(arri_air_info.flight_price) + int(depa_air_info.flight_price)

        try: 
            Passenger.objects.create(
                first_name    = data['first_name'],
                last_name     = data['last_name'],
                nationality   = data['nationality'],
                date_of_birth = data['birth'],
                gender        = data['gender']
            )

        except KeyError:
            return JsonResponse({"message":"KEYERROR"}, status=401)

        if user.point < total_price_int :
            return JsonResponse({"message":"NOT ENOUGH POINTS"}, status=401)

        if arri_air_info.remain_seats == 0 or depa_air_info.remain_seats == 0:
            return JsonResponse({"message":"THE SEATS ARE SOLD OUT"}, status=401)

        user.point -= total_price_int
        user.save()
        arri_air_info.remain_seats -= 1
        depa_air_info.remain_seats -= 1
        depa_air_info.save()
        arri_air_info.save()
        
        return JsonResponse({"message":"CREATED!"}, status=201)