from django.shortcuts import redirect
from django.contrib import messages
from cms.utils.get_tiktoks_from_account import get_new_tiktoks_from_account
from cms.models import PieceOfContent, ContentType, Settings

def check_tiktok_view(request):
    """
    View to fetch and save new TikTok videos from the configured account.
    """
    try:
        # Get TikTok username from settings
        settings = Settings.objects.first()
        if not settings or not settings.tiktok_account_name:
            messages.error(request, "TikTok account name not configured in settings")
            return redirect('settings')
            
        # Fetch new videos
        new_videos = get_new_tiktoks_from_account(settings.tiktok_account_name)
        
        # Save new videos to database
        saved_count = 0
        for video in new_videos:
            PieceOfContent.objects.create(
                link=video['link'],
                content_type=ContentType.TIKTOK,
                likes=video['likes'],
                views=video['views']
            )
            saved_count += 1
            
        if saved_count > 0:
            messages.success(request, f"Successfully added {saved_count} new TikTok videos")
        else:
            messages.info(request, "No new TikTok videos found")
            
    except Exception as e:
        messages.error(request, f"Error checking TikTok videos: {str(e)}")
        
    return redirect('project_list')
