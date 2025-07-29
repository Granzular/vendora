from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
        path("<pk>/detail/",views.detailView,name="detail"),
        path("categories/",views.CategoryListView.as_view(),name="categories"),
        path("categories/<category_name>/",views.category_products_view,name="category_products"),
        ]
