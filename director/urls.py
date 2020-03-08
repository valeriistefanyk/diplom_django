from django.urls import path
from director import views

urlpatterns = [
    path('', views.hello_mess, name='hello-message'),
]