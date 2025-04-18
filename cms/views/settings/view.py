from django.shortcuts import render, redirect
from django.contrib import messages
from cms.models import Settings

def settings_view(request):
    # Get or create the singleton settings instance
    settings, created = Settings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        settings.local_projects_folder = request.POST.get('local_projects_folder', '')
        settings.github_token = request.POST.get('github_token', '')
        settings.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    return render(request, 'settings/view.html', {
        'settings': settings,
        'github_token_placeholder': '••••••••••••••••' if settings.github_token else ''
    })
