from django.urls import path
from administrator.views import show_something

urlpatterns = [
    path('', show_something),
]