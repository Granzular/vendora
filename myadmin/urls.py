from django.urls import path
from . import views

app_name = "myadmin"

urlpatterns = [
        path('dashboard/',views.DashboardView.as_view(),name="dashboard"),
        path('api/live-sales/',views.sales_view,name='live-sales'),
        path('dashboard/product/',views.product_view,name="product"),
        path('dashboard/inventory/',views.inventory_view,name="inventory"),
        path('dashboard/category/',views.category_view,name="category"),


        ]
