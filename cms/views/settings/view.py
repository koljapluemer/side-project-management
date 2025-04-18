from django.shortcuts import render, redirect
from django.contrib import messages
from cms.models import Settings

def settings_view(request):
    # Get or create the singleton settings instance
    settings, created = Settings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        settings.local_projects_folder = request.POST.get('local_projects_folder', '')
        settings.github_token = request.POST.get('github_token', '')
        settings.tiktok_account_name = request.POST.get('tiktok_account_name', '')
        settings.tiktok_ms_token = request.POST.get('tiktok_ms_token', '')
        settings.twitter_account_name = request.POST.get('twitter_account_name', '')
        settings.reddit_account_name = request.POST.get('reddit_account_name', '')
        settings.hn_account_name = request.POST.get('hn_account_name', '')
        settings.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    return render(request, 'settings/view.html', {
        'settings': settings,
        'github_token_placeholder': '••••••••••••••••' if settings.github_token else '',
        'tiktok_ms_token_placeholder': '••••••••••••••••' if settings.tiktok_ms_token else ''
    })
