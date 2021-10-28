import json
import jwt

from django.test         import TestCase, Client
from django.db           import transaction

from my_settings         import SECRET_KEY, ALGORITHM
from reservations.models import Reservation, Airline, Airport
from users.models        import User

class TestCase(TestCase):
    @transaction.atomic
    def setUp(self):
        User.objects.bulk_create([
            User(
                id            = 1,
                name          = "현우",
                email         = "msm@naver.com",
                kakao_id      = "1",
                point         = "500000",
                profile_image = "profile1.jpg"
            ),
            User(
                id            = 2,
                name          = "현순",
                email         = "smsm@naver.com",
                kakao_id      = "2",
                point         = "50000000",
                profile_image = "profile2.jpg"
            )
            ])

        self.token = jwt.encode({'id':User.objects.get(kakao_id="1").id}, SECRET_KEY, algorithm=ALGORITHM)
        self.token2 = jwt.encode({'id':User.objects.get(kakao_id="1").id}, SECRET_KEY, algorithm=ALGORITHM)

        Airport.objects.bulk_create([
            Airport(
                id       = 1,
                name     = "김포",
                eng_name = "KMP"
            ),
            Airport(
                id       = 2,
                name     = "제주",
                eng_name = "JEJU"
            )
        ])

        Airline.objects.bulk_create([
            Airline(
                id       = 1,
                name     = "위코드항공",
                eng_name = "wecode",
                logo_url = "we_url"
            ),
            Airline(
                id       = 2,
                name     = "니코드항공",
                eng_name = "necode",
                logo_url = "ne_url"
            )
        ])

        Reservation.objects.bulk_create([
            Reservation(
                id                = 1,
                flight_code       = "we123",
                depart_time       = "10:20",
                arrive_time       = "12:20",
                start_date        = "2021-11-03",
                end_date          = "2021-11-03",
                remain_seats      = 30,
                seat_class        = "일반",
                airline_id        = 1,
                airport_arrive_id = 2,
                airport_depart_id = 1,
                flight_price      = 10000
            ),
            Reservation(
                id                = 2,
                flight_code       = "ne123",
                depart_time       = "11:20",
                arrive_time       = "13:20",
                start_date        = "2021-11-04",
                end_date          = "2021-11-04",
                remain_seats      = 40,
                seat_class        = "비지니스",
                airline_id        = 2,
                airport_arrive_id = 1,
                airport_depart_id = 2,
                flight_price      = 20000
            ),
            Reservation(
                id                = 3,
                flight_code       = "ne123",
                depart_time       = "11:20",
                arrive_time       = "13:20",
                start_date        = "2021-11-04",
                end_date          = "2021-11-04",
                remain_seats      = 40,
                seat_class        = "비지니스",
                airline_id        = 2,
                airport_arrive_id = 1,
                airport_depart_id = 2,
                flight_price      = 6000000
            ),
            Reservation(
                id                = 4,
                flight_code       = "ne123",
                depart_time       = "11:20",
                arrive_time       = "13:20",
                start_date        = "2021-11-04",
                end_date          = "2021-11-04",
                remain_seats      = 0,
                seat_class        = "비지니스",
                airline_id        = 2,
                airport_arrive_id = 1,
                airport_depart_id = 2,
                flight_price      = 600
            )
        ])

    def tearDown(self):
        User.objects.all().delete()
        Airport.objects.all().delete()
        Airline.objects.all().delete()
        Reservation.objects.all().delete()

    def test_success_get_reservation_info(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.token}
        response     = client.get('/payments/payment?depa-air=1&arri-air=2', content_type='application/json', **header)
        access_token = jwt.decode(self.token, SECRET_KEY, algorithms=ALGORITHM)
        user         = User.objects.get(id = access_token['id'])
        self.assertEqual(response.json(),
        {
            "user_info": {
                "name"  : user.name,
                "email" : user.email
            },
            "depature_airplane_info": {
                "departure_airport"     : "김포",
                "departure_airport_eng" : "KMP",
                "departure_time"        : "10:20:00",
                "arrival_airport"       : "제주",
                "arrival_airport_eng"   : "JEJU",
                "arrival_time"          : "12:20:00",
                "depa_airline_name"     : "위코드항공",
                "depa_airline_logo"     : "we_url",
                "airplane_code"         : "we123",
                "seat_class"            : "일반",
                "price"                 : 10000,
                "start_date"            : "2021-11-03",
                "remain_seats"          : 30,
                "flight_duration"       : "2:00:00"
            },
            
            "arrival_airplane_info": {
                "departure_airport"     : "제주",
                "departure_airport_eng" : "JEJU",
                "departure_time"        : "11:20:00",
                "arrival_airport"       : "김포",
                "arrival_airport_eng"   : "KMP",
                "arrival_time"          : "13:20:00",
                "depa_airline_name"     : "니코드항공",
                "depa_airline_logo"     : "ne_url",
                "airplane_code"         : "ne123",
                "seat_class"            : "비지니스",
                "price"                 : 20000,
                "start_date"            : "2021-11-04",
                "remain_seats"          : 40,
                "flight_duration"       : "2:00:00"
            },
            "total_price": {
                "total_price": 30000
            }
        }
        )

        self.assertEquals(response.status_code, 200)
    
    def test_success_create_passenger(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.token}
        data     = {
            "first_name"    : 'first_name',
            "last_name"     : 'last_name',
            "nationality"   : 'nationality',
            "birth"         : '2010-10-11',
            "gender"        : 'True'
        }
        response = client.post('/payments/payment?depa-air=1&arri-air=2', json.dumps(data), content_type='application/json', **header)

        self.assertEqual(response.json(),
        {
                "message":"CREATED!"
        })
        
        self.assertEquals(response.status_code,201)
    
    def test_fail_create_passenger_keterror(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.token}
        data     = {
            "first_name"    : 'first_name',
            "last_ame"      : 'last_name',
            "nationality"   : 'nationality',
            "birth"         : '2010-10-11',
            "gender"        : 'True'
        }
        response = client.post('/payments/payment?depa-air=1&arri-air=2', json.dumps(data), content_type='application/json', **header)

        self.assertEqual(response.json(),
        {
                "message":"KEYERROR"
        })

    def test_fail_payment_not_enough_money(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.token}
        data     = {
            "first_name"    : 'first_name',
            "last_name"     : 'last_name',
            "nationality"   : 'nationality',
            "birth"         : '2010-10-11',
            "gender"        : 'True'
        }
        response = client.post('/payments/payment?depa-air=1&arri-air=3', json.dumps(data), content_type='application/json', **header)

        self.assertEqual(response.json(),
        {
            "message":"NOT ENOUGH POINTS"
        })
    
    def test_fail_payment_not_enough_seats(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.token2}
        
        data     = {
            "first_name"    : 'first_name',
            "last_name"     : 'last_name',
            "nationality"   : 'nationality',
            "birth"         : '2010-10-11',
            "gender"        : 'True'
        }
        response = client.post('/payments/payment?depa-air=1&arri-air=4', json.dumps(data), content_type='application/json', **header)

        self.assertEqual(response.json(),
        {
            "message":"THE SEATS ARE SOLD OUT"
        })