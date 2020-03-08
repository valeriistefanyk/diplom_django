from django.urls import path
from engineer import views


app_name = 'engineer'

urlpatterns = [
    path('', views.hello_mess, name='hello-message'),
    path('raports/', views.showRaports, name='raports'),
]