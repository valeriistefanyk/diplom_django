from django.urls import path
from engineer import views


app_name = 'engineer'

urlpatterns = [
    path('', views.hello_page, name='home-page'),
    path('reports/', views.showReports, name='reports'),
    path('drivers/', views.show_drivers, name='drivers'),
    path('drivers/<str:username>/', views.show_drivers_detail, name='driver_detail'),
    path('workdays/', views.work_days, name='work_days'),
    path('fix-machines/', views.show_fix_machines, name='fix_machines'),
]