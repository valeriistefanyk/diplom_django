from django.urls import path
from director import views


app_name = 'director'

urlpatterns = [
    path('', views.hello_mess, name='home-page'),
    path('reports/', views.show_reports, name='reports'),
    path('statistics/', views.show_statistics, name='statistics'),
    path('employees/', views.show_employees, name='employees'),
]