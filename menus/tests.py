from django.test import TestCase, Client

import json

from .models     import Menu, SubProduct, StarRating, ProductStar

class Test(TestCase):
    def setUp(self):
        Menu.objects.bulk_create([
            Menu(id=1, name="홈"),
            Menu(id=2, name="집"),
            Menu(id=3, name="공원"),
            Menu(id=4, name="학교"),
            ])

        SubProduct.objects.bulk_create([
            SubProduct(
                id      = 1, 
                sub_name = "특가", 
                name    = "제주도", 
                price   = "13000", 
                image   = "jeju.url",
                menu_id = 1
            ),
            SubProduct(
                id       = 2,
                sub_name = '초특가',
                name     = "부산",
                price    = "20000",
                image    = "busan.url",
                menu_id  = 2
            ),
        ])
  

        StarRating.objects.bulk_create([
            StarRating(
                id     = 1,
                rating = 1
            ),
            StarRating(
                id     = 2,
                rating = 2
            ),
            StarRating(
                id     = 3,
                rating = 3
            ),
            StarRating(
                id     = 4,
                rating = 4
            ),
            StarRating(
                id     = 5,
                rating = 5
            )
        ])

        ProductStar.objects.bulk_create([
            ProductStar(
                id             = 1,
                sub_product_id = 1,
                Rate_id        = 1
            ),
            ProductStar(
                id             = 2,
                sub_product_id = 1,
                Rate_id        = 2
            ),
            ProductStar(
                id             = 3,
                sub_product_id = 2,
                Rate_id        = 3
            ),
        ])

    def tearDown(self):
        Menu.objects.all().delete()
        SubProduct.objects.all().delete()
        StarRating.objects.all().delete()
        ProductStar.objects.all().delete()

    def test_get_item_in_menu_secces(self):
        client = Client()
        response = client.get('/menus/menu')
        self.assertEqual(response.json(),
            {
            "menu": [
                {
                    "id": 1,
                    "list": "홈"
                },
                {
                    "id": 2,
                    "list": "집"
                },
                {
                    "id": 3,
                    "list": "공원"
                },
                {
                    "id": 4,
                    "list": "학교"
                }
                    ]
            }
        )
        self.assertEquals(response.status_code, 201)

    def test_post_item_in_menu_success(self):
        client = Client()
        data = {
            "name" : "홈"
            }
        response  = client.post('/menus/menu', json.dumps(data), content_type='applications/json')
        
        self.assertEqual(response.json(),
            {
              "message":"created!"
            }
        )
        self.assertEquals(response.status_code, 201)

    def test_fail_post_item_in_menu_keyerror(self):
        client = Client()
        header= {}
        response  = client.post('/menus/menu', content_type='applications/json', **header)
        
        self.assertEqual(response.json(),
            {
              "message": "KEYERROR"
            }
        )
        self.assertEquals(response.status_code, 401)

    def test_fail_post_item_in_subproudct_keyerror(self):
        client = Client()
        data= {"1":"1"}
        response  = client.post('/menus/subproduct?name=서브', json.dumps(data) ,content_type='applications/json')
        
        self.assertEqual(response.json(),
            {
              "message": "KEYERROR"
            }
        )
        self.assertEquals(response.status_code, 401)
    
    def test_success_post_create_subproduct_(self):
        client = Client()
        data = {
            "id"       : "1",
            "sub_name" : "특가",
            "name"     : "제주도",
            "price"    : "13000",
            "image"    : "image.url"
        }

        response = client.post('/menus/subproduct?name=서브', json.dumps(data), content_type='applications/json')
        
        self.assertEqual(response.json(),
            {
              "message":"created!"
            }
        )
        self.assertEquals(response.status_code, 201)
    
    def test_success_get_item_in_subproduct(self):
        client = Client()
        response = client.get('/menus/subproduct', content_type='applications/json')

        self.assertEqual(response.json(),
        {
        "product": [
            {
                "id": 1,
                "category": "특가",            
                "title": "제주도",
                "original": 13000,
                "discount": 10400,
                "img_url": "jeju.url",
                "star": 2,
                "review_count": 2
            },
            {
                "id": 2,
                "category": "초특가",            
                "title": "부산",
                "original": 20000,
                "discount": 16000,
                "img_url": "busan.url",
                "star": 3,
                "review_count": 1
            },
        ]}
        )
        self.assertEquals(response.status_code, 201)
