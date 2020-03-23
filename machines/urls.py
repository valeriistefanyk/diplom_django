from django.urls import path 
from machines import views


app_name = 'machines'

urlpatterns = [
    path('', views.all_machines, name='all-machines'),
    path('detail/', views.show_detail_machines, name='detail_machines'),
    path('<int:id>/', views.detail_machine, name='detail'),
    path('description/', views.show_machines_description, name='show_machine_description'),
]