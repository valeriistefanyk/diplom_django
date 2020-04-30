from django.urls import path
from director import views


app_name = 'director'

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('reports/', views.show_reports, name='reports'),
    path('reports/<int:report_id>/', views.show_report_detail, name='report-detail'),
    path('statistics/', views.show_statistics, name='statistics'),
    path('statistics/<int:driver_id>/', views.brigade_statistic, name='brigade-statistic'),
    path('employees/', views.show_employees, name='employees'),
    path('machines/', views.all_machines, name='all-machines'),
]


