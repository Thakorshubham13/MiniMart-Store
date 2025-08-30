from django.urls import path
from . import views

urlpatterns = [
    path('',views.add_product, name='add_product'),
    path('productlist/',views.list_product, name='list_product')
]
