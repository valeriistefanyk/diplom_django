from django.urls import path
from director import views


app_name = 'director'

urlpatterns = [
    path('', views.hello_mess, name='home-page'),
]