from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from main import views, settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('login/', views.mylogin, name='mylogin'),
    path('logout/', views.mylogout, name='mylogout'),

    path('machines/', include('machines.urls')),
    path('driver/', include('senior_driver.urls')),
    path('engineer/', include('engineer.urls')),
    path('director/', include('director.urls')),

    path('administrator/', include('administrator.urls')),
]

from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns


from django.contrib.staticfiles.urls import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)