from django.urls import path
from .views  import views,api

app_name = "orders"

urlpatterns = [
        path("<status>/list/",views.orders_list_view,name="list"),
        path("<pk>/detail/",views.orders_detail_view,name="detail"),
        path("cart_view/",views.cart_view,name="cart_view"),
        
        ]
## DRF APIs View
urlpatterns += [
        path("api/cart/",api.CartView.as_view(),name="api-cart-view"),
        path("api/cart/<int:pk>",api.CartView.as_view(),name="api-cart-patch-put-delete")
        ]
