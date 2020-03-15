from django.urls import path
from senior_driver import views


app_name = 'driver'

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('report/', views.make_report, name='report'),
    path('myreports/', views.show_my_reports, name='my_reports'),
    path('machines/', views.show_machines, name='machines'),
    path('about/', views.about, name='about'),
]