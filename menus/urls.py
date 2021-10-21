from django.urls import path

from .views      import MenuView, SubProductView, PlaneCategory

urlpatterns = [
    path("/menu", MenuView.as_view()),
    path("/subproduct", SubProductView.as_view()),
    path("/planecategory", PlaneCategory.as_view())
]