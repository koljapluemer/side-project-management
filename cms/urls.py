from django.urls import path
from cms.views.settings.view import settings_view
from cms.views.projects.list.list import ProjectListView
from cms.views.content.check_tiktok import check_tiktok_view
from cms.views.actions.actions import actions_view
from cms.views.content.list import ContentListView
from cms.views.content.check_twitter import check_twitter_view
from cms.views.dashboard.dashboard import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('settings/', settings_view, name='settings'),
    path('check-tiktok/', check_tiktok_view, name='check_tiktok'),
    path('check-twitter/', check_twitter_view, name='check_twitter'),
    path('actions/', actions_view, name='actions'),
    path('content/', ContentListView.as_view(), name='content_list'),
]
