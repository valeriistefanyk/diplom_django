from django.urls import path
from senior_machinist import views


app_name = 'machinist'

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('machine/', views.my_machine, name='machine'),
    path('machine/status/', views.machine_status, name='machine-status'),
    path('contact/', views.management_contact, name='management-contact'),
    path('members/', views.brigade_members, name='brigade-members'),
    path('route-sheet/', views.route_sheet, name='route-sheet'),
    path('route-sheet/machine-info', views.machine_working_fill, name='machine-fill'),
    path('show-route-sheets/', views.show_route_sheet, name='show-route-sheet'),
    path('route-sheet/<int:route_sheet_id>/', views.route_sheet_detail, name='route-sheet-detail'),
]
