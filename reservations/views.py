import json
import random

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from reservations.models    import AirlinesSchedule, AirplaneTaxes, Airport, FlightSchedule, Reservation, SeatClass



class ReservationView(View):
    def get(self, request):
        try:
            data        = request.GET
            arrival     = data['arrival']
            date        = data['date']
            departure   = data['departure']
            sort        = data['sort']
            time_option = data.getlist('timeOption')
            passenger   = data['passenger']

            Airlines = AirlinesSchedule.objects.select_related(
                'departure_airport','arrival_airport','airline').filter(
                departure_airport__code=departure,arrival_airport__code=arrival,departure_date=date,
                ).filter(time_frame__in=time_option,flight_prices__remaining_seat__gte=passenger,
                )

            sort_option = {
                'departureTime:asc'  : 'departure_time',
                'departureTime:desc' : '-departure_time',
                'price:asc'          : 'flight_prices__price'
            }

            airline_info = [{
                'id'               : airline.id,
                'airline'          : airline.airline.name,
                'airline_logo'     : airline.airline.image_url,
                'flightCode'       : airline.flight_code,
                'departureAirport' : airline.daparture_airport,
                'arrivalAirpoet'   : airline.Arrival_airport,
                'departureTime'    : airline.departure_time,
                'arrivalTime'      : airline.arrival_time,
                'durationTime'     : airline.duration_time,
                'status'           : airline.flight_prices.get().status.name,
                'remainingSeat'    : airline.flight_prices.get().remaining_seat,
                'price'            : airline.flight_prices.get().price
            } for airline in Airlines.order_by(sort_option[sort])]

            return JsonResponse({
                'date'                 : date,
                'departureAirportName' : Airlines[0].departure_airport.name,
                'departureAirportCode' : departure,
                'arrivalAirportName'   : Airlines[0].arrival_airport.name,
                'arrivalAirportCode'   : arrival,
                'flights'              : airline_info
            }, status=200)
        
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except IndexError:
            return JsonResponse({
                'message'              : 'INDEX_ERROR',
                'date'                 : date,
                'departureAirportCode' : departure,
                'arrivalAirportCode'   : arrival,
                }, status=400)

    
class AirplaneTaxeView(View):  
    def get(self, request):
        airline_price  = Reservation.objects.get(airline_price = request.airline)
        fuel_surcharge = airline_price * 0.1
        customs_duty   = 8000
        ticketing_fee  = 0
        total_price    = airline_price + AirplaneTaxes.aggregate(total_price=('price'))

        return JsonResponse({
            'fuel_surcharge' : fuel_surcharge,
            'customs_duty'   : customs_duty,
            'ticketing_fee'  : ticketing_fee,
            'total_price'    : total_price,},
             status = 200)


