from django.db           import models

class Menu(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "menus"

class Product(models.Model):
    name  = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    menu  = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = "products"

class SubProduct(models.Model):
    sub_name = models.CharField(max_length=50)
    name     = models.CharField(max_length=50)
    price    = models.IntegerField()
    image    = models.URLField(max_length=500)
    menu     = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = "sub_products"

class StarRating(models.Model):
    rating = models.IntegerField()

    class Meta:
        db_table = "star_ratings"

class ProductStar(models.Model):
    sub_product = models.ForeignKey(SubProduct, on_delete=models.CASCADE)
    Rate        = models.ForeignKey(StarRating, on_delete=models.CASCADE)

    class Meta:
        db_table = "sub_products_stars"