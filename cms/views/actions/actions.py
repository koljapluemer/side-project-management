from django.shortcuts import render, redirect
from django.contrib import messages
from cms.models import Settings
from cms.utils.sync_github_account import sync_github_repositories
from cms.utils.sync_local_folders import sync_local_folders
from cms.views.projects.delete_all import delete_all_projects

def sync_local_folders_view(request):
    try:
        settings = Settings.objects.first()
        if not settings or not settings.local_projects_folder:
            raise ValueError("Local projects folder not configured in settings")
            
        sync_local_folders(settings.local_projects_folder)
        messages.success(request, "Successfully synced local folders")
    except ValueError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f"Error syncing local folders: {str(e)}")
    return redirect('actions')

def delete_all_projects_view(request):
    try:
        count = delete_all_projects()
        messages.success(request, f"Successfully deleted {count} projects")
    except Exception as e:
        messages.error(request, f"Error deleting projects: {str(e)}")
    return redirect('actions')

def sync_github_view(request):
    try:
        num_repos = sync_github_repositories()
        messages.success(request, f"Successfully synced {num_repos} GitHub repositories")
    except ValueError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f"Error syncing GitHub repositories: {str(e)}")
    return redirect('actions')

def actions_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'check_tiktok':
            settings = Settings.objects.first()
            if not settings or not settings.tiktok_account_name:
                messages.error(request, "Please configure your TikTok username in settings first")
                return redirect('settings')
            return redirect('check_tiktok')
            
        messages.error(request, "Invalid action")
        return redirect('actions')
    
    return render(request, 'actions/actions.html')
