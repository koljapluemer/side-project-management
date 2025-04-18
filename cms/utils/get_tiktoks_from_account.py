from typing import List, Dict
import asyncio
import os
from TikTokApi import TikTokApi
from django.utils import timezone
from cms.models import PieceOfContent, ContentType, Settings
from asgiref.sync import sync_to_async

@sync_to_async
def get_settings():
    return Settings.objects.first()

@sync_to_async
def get_existing_links():
    return set(PieceOfContent.objects.filter(
        content_type=ContentType.TIKTOK
    ).values_list('link', flat=True))

async def get_new_tiktoks_from_account(username: str, max_videos: int = 10) -> List[Dict]:
    """
    Fetch new TikTok videos from a public account that haven't been added to the database yet.
    
    Args:
        username (str): The TikTok username to fetch videos from (without @)
        max_videos (int): Maximum number of videos to fetch (default: 10)
        
    Returns:
        List[Dict]: List of dictionaries containing video information
    """
    try:
        # Get ms_token from settings
        settings = await get_settings()
        if not settings or not settings.tiktok_ms_token:
            print("Error: TikTok ms_token not configured in settings")
            return []
            
        ms_token = settings.tiktok_ms_token
        print(f"Starting TikTok fetch for user: {username}")
        print(f"Using ms_token: {ms_token[:10]}...")
            
        # Initialize API with minimal configuration
        api = TikTokApi()
        
        # Create session with basic settings
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3
        )
        print("Created session")
        
        try:
            # Get user info first
            user = api.user(username)
            user_data = await user.info()
            print(f"Got user info: {user_data}")
            
            # Get existing video links from database
            existing_links = await get_existing_links()
            print(f"Found {len(existing_links)} existing videos in database")
            
            videos = []
            count = 0
            
            # Process videos
            async for video in user.videos(count=max_videos):
                count += 1
                print(f"Processing video {count}/{max_videos}")
                
                # Get video data as dict
                video_data = video.as_dict
                print(f"Video data: {video_data}")
                
                video_link = f"https://www.tiktok.com/@{username}/video/{video_data['id']}"
                print(f"Video link: {video_link}")
                
                # Skip if video already exists in database
                if video_link in existing_links:
                    print(f"Skipping existing video: {video_link}")
                    continue
                
                videos.append({
                    'link': video_link,
                    'likes': video_data.get('stats', {}).get('diggCount', 0),
                    'views': video_data.get('stats', {}).get('playCount', 0),
                    'description': video_data.get('desc', ''),
                    'created_at': timezone.datetime.fromtimestamp(video_data.get('createTime', 0))
                })
                print(f"Added new video: {video_link}")
            
            print(f"Total new videos found: {len(videos)}")
            return videos
            
        finally:
            # Clean up
            await api.stop_playwright()
            
    except Exception as e:
        print(f"Error fetching TikTok videos: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return []

def sync_get_new_tiktoks_from_account(username: str, max_videos: int = 10) -> List[Dict]:
    """
    Synchronous wrapper for the async TikTok fetching function.
    """
    return asyncio.run(get_new_tiktoks_from_account(username, max_videos))
