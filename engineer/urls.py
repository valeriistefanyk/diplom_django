from django.urls import path
from engineer import views

urlpatterns = [
    path('', views.hello_mess, name='hello-message')
]