import datetime

from django.test import TestCase, Client

from .models import Airline, Airport, Reservation

class Reservation_List_Test(TestCase):
    maxDiff = None

    def setUpClass(self):
        client = Client()
        Airline.objects.create(
            id        = 1,
            name      = '대한',
            image_url = 'https://wecode.co.kr/',

            id        = 2,
            name      ='민국',
            image_url = 'https://wecode.co.kr/',

            id        = 3,
            name      = '만세',
            image_url = 'https://wecode.co.kr/'
        )

        Airport.objects.bulk_create([
            Airport(
                id   = 1,
                name = '김포',
                eng_name =  'GMP'
            ),
            Airport(
                id   = 2,
                name = '제주',
                eng_name = 'CJU'
            )
        ])

        Reservation.objects.bulk_create([
            Reservation(
                id                   = 1,
                flight_code          = 'WE001',
                departure_date       = '2021-03-12',
                arrival_date         = '2021-03-12',
                departure_time       = '05:00:00',
                arrival_time         = '06:10:00',
                duration_time        = '01:10:00',
                airline_id           = 1,
                departure_airport_id = 1,
                arrival_airport_id   = 2,
                time_frame           = 1
            ),
            Reservation(
                id                   = 2,
                flight_code          = 'WE002',
                departure_date       = '2021-03-12',
                arrival_date         = '2021-03-12',
                departure_time       = '10:00:00',
                arrival_time         = '11:10:00',
                duration_time        = '01:10:00',
                airline_id           = 1,
                departure_airport_id = 1,
                arrival_airport_id   = 2,
                time_frame           = 2
            ),
            Reservation(
                id                   = 3,
                flight_code          = 'WE003',
                departure_date       = '2021-03-12',
                arrival_date         = '2021-03-12',
                departure_time       = '11:00:00',
                arrival_time         = '12:10:00',
                duration_time        = '01:10:00',
                airline_id           = 1,
                departure_airport_id = 1,
                arrival_airport_id   = 2,
                time_frame           = 2
            ),
        ])

    def tearDownClass(cls):
        Airline.objects.all().delete()
        Airport.objects.all().delete()
        Reservation.objects.all().delete()

    def test_flight_get_success(self):
        response = self.client.get('/flight?departure=GMP&arrival=CJU&date=2021-03-12&sort=departureTime:asc&timeOption=1&timeOption=2&timeOption=3&timeOption=4&passenger=3', content_type = 'application/json')

        self.assertEqual(response.json(),{
            'date'                 : '2021-03-12',
            'departureAirportName' : '김포',
            'departureAirportCode' : 'GMP',
            'arrivalAirportName'   : '제주',
            'arrivalAirportCode'   : 'CJU',
            'flights'              : [
                {
                    'id'           : 1,
                    'airline'      : 'wecode',
                    'airline_logo' : 'https://wecode.co.kr/',
                    'flightCode'   : 'WE001',
                    'departureTime': '05:00:00',
                    'arrivalTime'  : '06:10:00',
                    'durationTime' : '01:10:00',
                    'status'       : '특가석',
                    'remainingSeat': 3,
                    'price'        : '38900.00'
                },
                {
                    'id'           : 2,
                    'airline'      : 'wecode',
                    'airline_logo' : 'https://wecode.co.kr/',
                    'flightCode'   : 'WE002',
                    'departureTime': '10:00:00',
                    'arrivalTime'  : '11:10:00',
                    'durationTime' : '01:10:00',
                    'status'       : '특가석',
                    'remainingSeat': 5,
                    'price'        : '36900.00'
                }
            ]
        })
        self.assertEqual(response.status_code, 200)

    def test_flight_sorting_success(self):
        response = self.client.get('/flight?departure=GMP&arrival=CJU&date=2021-03-12&sort=price:asc&timeOption=1&timeOption=2&timeOption=3&timeOption=4&passenger=3', content_type = 'application/json')

        self.assertEqual(response.json(),{
            'date'                 : '2021-03-12',
            'departureAirportName' : '김포',
            'departureAirportCode' : 'GMP',
            'arrivalAirportName'   : '제주',
            'arrivalAirportCode'   : 'CJU',
            'flights'              : [
                {
                    'id'           : 2,
                    'airline'      : 'wecode',
                    'airline_logo' : 'https://wecode.co.kr/',
                    'flightCode'   : 'WE002',
                    'departureTime': '10:00:00',
                    'arrivalTime'  : '11:10:00',
                    'durationTime' : '01:10:00',
                    'status'       : '특가석',
                    'remainingSeat': 5,
                    'price'        : '36900.00'
                },
                {
                    'id'           : 1,
                    'airline'      : 'wecode',
                    'airline_logo' : 'https://wecode.co.kr/',
                    'flightCode'   : 'WE001',
                    'departureTime': '05:00:00',
                    'arrivalTime'  : '06:10:00',
                    'durationTime' : '01:10:00',
                    'status'       : '특가석',
                    'remainingSeat': 3,
                    'price'        : '38900.00'
                }
            ]
        })
        self.assertEqual(response.status_code, 200)