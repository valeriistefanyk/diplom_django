from django.urls import path
from senior_driver import views

urlpatterns = [
    path('', views.hello_mess, name='hello-message'),
    path('about', views.about, name='about-message'),
]