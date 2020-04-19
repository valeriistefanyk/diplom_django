from django.urls import path
from engineer import views


app_name = 'engineer'

urlpatterns = [
    path('', views.hello_page, name='home-page'),
    path('unforwarded_reports/', views.show_unforwarded_reports, name='unforwarded_reports'),
    path('forwarded_reports/', views.show_forwarded_reports, name='forwarded_reports'),
    path('drivers/', views.show_drivers, name='drivers'),
    path('drivers/<str:username>/', views.show_drivers_detail, name='driver_detail'),
    path('workdays/', views.work_days, name='work_days'),
    path('fix-machines/', views.show_fix_machines, name='fix_machines'),
    path('machines/', views.all_machines, name='all-machines'),
]