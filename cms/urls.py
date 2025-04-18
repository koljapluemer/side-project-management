from django.urls import path
from cms.views.settings.view import settings_view
from cms.views.projects.list.list import ProjectListView
from cms.views.content.check_tiktok import check_tiktok_view
from cms.views.actions.actions import actions_view

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('settings/', settings_view, name='settings'),
    path('check-tiktok/', check_tiktok_view, name='check_tiktok'),
    path('actions/', actions_view, name='actions'),
]
