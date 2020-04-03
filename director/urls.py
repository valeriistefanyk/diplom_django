from django.urls import path
from director import views


app_name = 'director'

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('reports/', views.show_reports, name='reports'),
    path('test_reports/', views.test_show_reports, name='test_reports'),
    path('statistics/', views.show_statistics, name='statistics'),
    path('test_statistics/', views.test_show_statistics, name='test_statistics'),
    path('employees/', views.show_employees, name='employees'),
]