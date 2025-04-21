from django.urls import path
from cms.views.settings.view import settings_view
from cms.views.projects.list import ProjectListView
from cms.views.projects.create_update import project_create_update
from cms.views.projects.view import ProjectDetailView
from cms.views.goatcounter_tracker.create_update import (
    GoatcounterTrackerCreateView,
    GoatcounterTrackerUpdateView
)
from cms.views.content.check_tiktok import check_tiktok_view
from cms.views.actions.actions import (
    actions_view, 
    sync_github_view, 
    delete_all_projects_view,
    sync_local_folders_view
)
from cms.views.content.list import ContentListView
from cms.views.content.check_twitter import check_twitter_view
from cms.views.dashboard.dashboard import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/create/', project_create_update, name='project_create'),
    path('projects/<int:pk>/update/', project_create_update, name='project_update'),
    path('projects/<int:project_pk>/goatcounter/create/', 
         GoatcounterTrackerCreateView.as_view(), 
         name='goatcounter_tracker_create'),
    path('projects/<int:project_pk>/goatcounter/<int:pk>/update/', 
         GoatcounterTrackerUpdateView.as_view(), 
         name='goatcounter_tracker_update'),
    path('settings/', settings_view, name='settings'),
    path('check-tiktok/', check_tiktok_view, name='check_tiktok'),
    path('check-twitter/', check_twitter_view, name='check_twitter'),
    path('actions/', actions_view, name='actions'),
    path('sync-github/', sync_github_view, name='sync_github'),
    path('sync-local-folders/', sync_local_folders_view, name='sync_local_folders'),
    path('delete-all-projects/', delete_all_projects_view, name='delete_all_projects'),
    path('content/', ContentListView.as_view(), name='content_list'),
]
