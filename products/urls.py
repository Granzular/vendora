from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
        path("<pk>/detail/",views.detailView,name="detail"),
        path("categories/",views.CategoryListView.as_view(),name="categories"),
        ]
