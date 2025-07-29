from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
        path("<status>/list/",views.orders_list_view,name="list"),
        path("<pk>/detail/",views.orders_detail_view,name="detail"),
        
        ]
