from django.urls import path 
from machines import views


app_name = 'machines'

urlpatterns = [
    path('', views.all_machines, name='all-machines'),
    path('<int:id>/', views.detail_machine, name='detail'),
    path('test/', views.show_machines_test, name='show_machines_test'),
]