from django.shortcuts import render, redirect
from django.contrib import messages
from cms.models import Settings

def settings_view(request):
    # Get or create the singleton settings instance
    settings, created = Settings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        settings.local_projects_folder = request.POST.get('local_projects_folder', '')
        settings.obsidian_projects_folder = request.POST.get('obsidian_projects_folder', '')
        settings.github_token = request.POST.get('github_token', '')
        settings.tiktok_account_name = request.POST.get('tiktok_account_name', '')
        settings.tiktok_ms_token = request.POST.get('tiktok_ms_token', '')
        settings.twitter_account_name = request.POST.get('twitter_account_name', '')
        settings.twitter_bearer_token = request.POST.get('twitter_bearer_token', '')
        settings.twitter_api_key = request.POST.get('twitter_api_key', '')
        settings.twitter_api_secret = request.POST.get('twitter_api_secret', '')
        settings.twitter_access_token = request.POST.get('twitter_access_token', '')
        settings.twitter_access_token_secret = request.POST.get('twitter_access_token_secret', '')
        settings.reddit_account_name = request.POST.get('reddit_account_name', '')
        settings.hn_account_name = request.POST.get('hn_account_name', '')
        settings.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    return render(request, 'settings/view.html', {
        'settings': settings,
        'github_token_placeholder': '••••••••••••••••' if settings.github_token else '',
        'tiktok_ms_token_placeholder': '••••••••••••••••' if settings.tiktok_ms_token else '',
        'twitter_bearer_token_placeholder': '••••••••••••••••' if settings.twitter_bearer_token else '',
        'twitter_api_key_placeholder': '••••••••••••••••' if settings.twitter_api_key else '',
        'twitter_api_secret_placeholder': '••••••••••••••••' if settings.twitter_api_secret else '',
        'twitter_access_token_placeholder': '••••••••••••••••' if settings.twitter_access_token else '',
        'twitter_access_token_secret_placeholder': '••••••••••••••••' if settings.twitter_access_token_secret else ''
    })
