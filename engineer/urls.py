from django.urls import path
from engineer import views


app_name = 'engineer'

urlpatterns = [
    path('', views.hello_mess, name='home-page'),
    path('reports/', views.showRaports, name='reports'),
    path('drivers/', views.show_drivers, name='drivers'),
    path('workdays/', views.work_days, name='work_days'),
]