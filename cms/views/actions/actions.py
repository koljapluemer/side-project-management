from django.shortcuts import render, redirect
from django.contrib import messages
from cms.models import Settings

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
