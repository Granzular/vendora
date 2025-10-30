from django.urls import path
from .views  import views,api

app_name = "orders"

urlpatterns = [
        path("<status>/list/",views.orders_list_view,name="list"),
        path("<pk>/detail/",views.orders_detail_view,name="detail"),
        path("cart-view/",views.cart_view,name="cart_view"),
        path("checkout/",views.checkout,name="checkout"),
        
        ]
## DRF APIs View
urlpatterns += [
        path("api/cart/",api.CartView.as_view(),name="api-cart-view"),
        path("api/cart/<int:pk>/",api.CartView.as_view(),name="api-cart-patch-put-delete"),

        path("api/cart/bulk-create/",api.bulk_create_cart,name="bulk-cart-create"),
        path("api/cart/bulk-update/",api.bulk_update_cart,name="bulk-cart-update"),
        path("api/cart/bulk-delete/",api.bulk_delete_cart,name="bulk-cart-delete"),

        path("api/cart/custom/",api.cart_view,name="custom-cart-get"),
        ]
