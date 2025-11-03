from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
        path("accounts/profile/",views.ProfileView.as_view(),name="profile"),
        path("accounts/login/",views.LoginView.as_view(),name='login'),
        path("accounts/logout/",views.logout_view,name='logout'),
        path("accounts/signup/",views.SignUpView.as_view(),name='signup'),
        path("accounts/confirm_email/",views.confirm_email_view,name='confirm_email'),
        path("accounts/verify_email/<secret_key>/",views.confirm_email_verification_view,name="verify_email"),
        path("notifications/",views.notification_list,name="notification_list"),
        path("notifications/<pk>/detail/",views.notification_detail,name="notification_detail"),
        ]
