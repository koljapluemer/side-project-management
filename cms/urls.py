from django.contrib import admin
from django.urls import path
from cms.views.settings.view import settings_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', settings_view, name='settings'),
]
