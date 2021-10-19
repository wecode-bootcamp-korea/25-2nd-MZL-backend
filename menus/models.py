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