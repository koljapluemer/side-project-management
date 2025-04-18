from django.urls import path
from cms.views.settings.view import settings_view
from cms.views.projects.list.list import ProjectListView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('settings/', settings_view, name='settings'),
]
