import jwt
import requests
import json

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class LoginView(View):
    def get(self, request):
        try:
            access_token = request.headers.get('Authorization')
            headers      = {'Authorization': f"Bearer {access_token}"}

            response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers = headers,
                timeout=3
                )

            user_info = response.json()

            if not User.objects.filter(kakao_id = user_info['id']).exists():

                User.objects.create(
                    kakao_id      = user_info['id'],
                    name          = user_info["kakao_account"]["profile"]["nickname"],
                    email         = user_info["kakao_account"].get("email"),
                    profile_image = user_info["properties"].get("profile_image")
                )

            token = jwt.encode({'id' : user_info['id']}, SECRET_KEY, algorithm=ALGORITHM)


            return JsonResponse({"message": "SUCCESS","token" : token}, status=201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)