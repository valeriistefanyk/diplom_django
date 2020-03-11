from django.urls import path
from engineer import views


app_name = 'engineer'

urlpatterns = [
    path('', views.hello_mess, name='home-page'),
    path('raports/', views.showRaports, name='raports'),
]