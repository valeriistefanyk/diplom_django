"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),

    path('login/', views.mylogin, name='mylogin'),
    path('logout/', views.mylogout, name='mylogout'),

    path('machines/', include('machines.urls')),
    path('driver/', include('senior_driver.urls')),
    path('engineer/', include('engineer.urls')),
    path('director/', include('director.urls')),

]

from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

# todo: add mediaroot