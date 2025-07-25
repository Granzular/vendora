from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
        path("accounts/login/",views.LoginView.as_view(),name='login'),
        path("accounts/logout/",views.logoutView,name='logout'),
        path("accounts/signup/",views.SignUpView.as_view(),name='signup'),
        ]
