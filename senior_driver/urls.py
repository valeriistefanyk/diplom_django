from django.urls import path
from senior_driver import views


app_name = 'driver'

urlpatterns = [
    path('', views.hello_mess, name='home-page'),
    path('about', views.about, name='about-message'),
]