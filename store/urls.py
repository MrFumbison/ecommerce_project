from django.urls import path
from .views import *

urlpatterns = [
    path("",store, name="store"),
    path("login",login, name="login"),
    path("cart/",cart, name="cart"),
    path("checkout/",checkout, name="checkout"),
    
     path("update_item/",updateitem, name="update_item"),
      path("process_order/",processorder, name="process_order"),
]
