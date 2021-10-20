from unittest.mock import MagicMock, patch
from django.test   import Client, TestCase

from .models       import User

class Test(TestCase):
    def setUp(self):
        User.objects.create(
            name          ='hyunwoo',
            kakao_id      = '123456',
            email         = 'hyun@naver.com',
            profile_image = "333222"
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_success_kakao_social_login(self, mocked_request):
        client = Client()

        class Kakao:
            def json(self):
                return{
                    "id":"123456",
                    "properties": {"profile_image": "333222"},
                    "kakao_account":{
                        "profile": {"nickname" : "hyunwoo"},
                                    "email" : "hyun@naver.com"}
                      }
        
        mocked_request.get = MagicMock(return_value=Kakao())
        header             = {'HTTP_Authorization' : 'token'}
        response           = client.get('/users/login', **header)

        self.assertEqual(response.status_code, 201)
        
    @patch("users.views.requests")
    def test_fail_unregistered_user_login(self, mocked_request):
        client = Client()

        class kakao:
            def json(self):
                return{
                    "KeyError": 'id'
                }
        
        mocked_request.get = MagicMock(return_value=kakao())
        header             = {'HTTP_Authorization' : 'token'}
        response           = client.get('/users/login', **header)

        self.assertEquals(response.status_code, 401)