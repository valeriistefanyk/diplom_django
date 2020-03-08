from django.urls import path 
from machines import views

urlpatterns = [
    path('', views.all_machines, name='machines'),
    path('<int:id>', views.detail_machine, name='detail'),
]