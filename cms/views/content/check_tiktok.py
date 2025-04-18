from django.shortcuts import redirect
from django.contrib import messages
from cms.utils.get_tiktoks_from_account import sync_get_new_tiktoks_from_account
from cms.models import PieceOfContent, ContentType, Settings
from django.utils import timezone

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
            
        # Remove @ if present in username
        username = settings.tiktok_account_name.lstrip('@')
            
        # Fetch new videos
        new_videos = sync_get_new_tiktoks_from_account(username)
        
        if not new_videos:
            messages.info(request, "No new TikTok videos found")
            return redirect('content_list')
        
        # Save new videos to database
        saved_count = 0
        for video in new_videos:
            try:
                PieceOfContent.objects.create(
                    link=video['link'],
                    content_type=ContentType.TIKTOK,
                    likes=video['likes'],
                    views=video['views'],
                    posted_at=video['created_at']
                )
                saved_count += 1
            except Exception as e:
                print(f"Error saving video {video['link']}: {str(e)}")
                continue
            
        if saved_count > 0:
            messages.success(request, f"Successfully added {saved_count} new TikTok videos")
        else:
            messages.info(request, "No new TikTok videos found")
            
    except Exception as e:
        print(f"Error in check_tiktok_view: {str(e)}")
        messages.error(request, f"Error checking TikTok videos: {str(e)}")
        
    return redirect('content_list')
