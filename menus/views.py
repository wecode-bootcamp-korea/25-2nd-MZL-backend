import json
import math

from django.http          import JsonResponse
from django.views         import View
from django.db.models     import Avg, Count

from .models              import Menu, SubProduct, StarRating, ProductStar
from reservations.models  import Reservation 

class MenuView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            Menu.objects.create(
                name = data['name']
            )

            return JsonResponse({"message":"created!"}, status=201)
        except KeyError:
            return JsonResponse({"message":"KEYERROR"}, status=401)
    
    def get(self, request):
        menu    = [{"id" : menu.id, "list": menu.name} for menu in Menu.objects.all()]
            
        return JsonResponse({"menu":menu}, status=201)

class SubProductView(View):
    def post(self, request):
        response = request.GET.get('name')
        data = json.loads(request.body)
        try:
            if response == "서브":              
                SubProduct.objects.create(
                    sub_name = data['sub_name'],
                    name     = data['name'],
                    price    = data['price'],
                    image    = data['image'],
                    menu_id  = data['id']
                )
                return JsonResponse({"message":"created!"}, status=201)

            elif response == "별":
                StarRating.objects.create(
                    rating = data["star"],
                    )

                return JsonResponse({"message":"created!"}, status=201)

            elif response == "중간":
                ProductStar.objects.create(
                            sub_product_id = data["sub_product_id"],
                            Rate_id = data["rate_id"]
                        )
                return JsonResponse({"message":"created!"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEYERROR"}, status=401)
            
    def get(self, request):
        rate_count = SubProduct.objects.all().annotate(average_rate=Avg('productstar__Rate'),sum_count=Count('productstar__Rate'))

        result = [
            {"id"           : product.id,
             "category"     : product.sub_name,
             "title"        : product.name,
             "original"     : product.price,
             "discount"     : int(product.price * 0.8),
             "img_url"      : product.image,
             "star"         : math.ceil(rate_count.filter(id = product.id).first().average_rate) if rate_count.filter(id = product.id).first().average_rate else 0,
             "review_count" : rate_count.filter(id = product.id).first().sum_count,
        } for product in SubProduct.objects.all()]

        return JsonResponse({"product":result}, status=201)

class PlaneCategory(View):
    def get(self, request):
        queryset = Reservation.objects.all().select_related('airport_depart','airport_arrive')

        result = [{
            "start_date"        : reservation.start_date,
            "end_date"          : reservation.end_date,
            "price"             : "{:,}".format(int(reservation.flight_price)+100000000),
            "departure_airport" : reservation.airport_depart.name,
            "arrive_airport"    : reservation.airport_arrive.name,
            "image"             : reservation.image
        }
            for reservation in queryset]
        
        return JsonResponse({"plane_info":result}, status=201)