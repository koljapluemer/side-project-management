from django.urls import path
from cms.views.settings.view import settings_view
from cms.views.projects.list import ProjectListView
from cms.views.projects.create_update import project_create_update
from cms.views.projects.view import ProjectDetailView
from cms.views.goatcounter_tracker.create_update import (
    GoatcounterTrackerCreateView,
    GoatcounterTrackerUpdateView
)
from cms.views.goatcounter_tracker.stats import update_goatcounter_stats
from cms.views.content.check_tiktok import check_tiktok_view
from cms.views.actions.actions import (
    actions_view, 
    sync_github_view, 
    delete_all_projects_view,
    sync_local_folders_view
)
from cms.views.content.list import ContentListView
from cms.views.content.check_twitter import check_twitter_view
from cms.views.dashboard.dashboard import DashboardView, UpdateStatsView
from cms.views.goals.view import goals_view
from cms.views.links.list import LinkListView
from cms.views.links.create_update import link_create_update, link_delete

urlpatterns = [
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    path('update-stats/', UpdateStatsView.as_view(), name='dashboard_update_stats'),
    
    # Projects
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/create/', project_create_update, name='project_create'),
    path('projects/<int:pk>/update/', project_create_update, name='project_update'),
    
    # Links
    path('links/', LinkListView.as_view(), name='link_list'),
    path('links/create/', link_create_update, name='link_create'),
    path('links/<int:pk>/update/', link_create_update, name='link_update'),
    path('links/<int:pk>/delete/', link_delete, name='link_delete'),
    
    # GoatCounter
    path('projects/<int:project_pk>/goatcounter/create/', 
         GoatcounterTrackerCreateView.as_view(), 
         name='goatcounter_tracker_create'),
    path('projects/<int:project_pk>/goatcounter/<int:pk>/update/', 
         GoatcounterTrackerUpdateView.as_view(), 
         name='goatcounter_tracker_update'),
    path('projects/<int:project_pk>/goatcounter/<int:tracker_pk>/stats/', 
         update_goatcounter_stats, 
         name='goatcounter_tracker_stats'),
    
    # Content
    path('content/', ContentListView.as_view(), name='content_list'),
    path('check-tiktok/', check_tiktok_view, name='check_tiktok'),
    path('check-twitter/', check_twitter_view, name='check_twitter'),
    
    # Actions
    path('actions/', actions_view, name='actions'),
    path('sync-github/', sync_github_view, name='sync_github'),
    path('sync-local-folders/', sync_local_folders_view, name='sync_local_folders'),
    path('delete-all-projects/', delete_all_projects_view, name='delete_all_projects'),
    
    # Settings
    path('settings/', settings_view, name='settings'),
    
    # Goals
    path('goals/', goals_view, name='goals'),
]
