from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
        path('',views.hero,name='hero'),
        path('store/',views.index,name='index'),
        #path('dashboard/',views.dashboard,name='dashboard'),
        ]
