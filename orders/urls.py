from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
        path("<status>/",views.orders_list_view,name="list"),
        
        ]
