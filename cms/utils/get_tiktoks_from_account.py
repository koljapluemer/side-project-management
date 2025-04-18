from typing import List, Dict
from tiktokapipy.api import TikTokAPI
from django.utils import timezone
from cms.models import PieceOfContent, ContentType

def get_new_tiktoks_from_account(username: str, max_videos: int = 10) -> List[Dict]:
    """
    Fetch new TikTok videos from a public account that haven't been added to the database yet.
    
    Args:
        username (str): The TikTok username to fetch videos from
        max_videos (int): Maximum number of videos to fetch (default: 10)
        
    Returns:
        List[Dict]: List of dictionaries containing video information
    """
    try:
        with TikTokAPI() as api:
            # Get user's videos
            user = api.user(username)
            videos = []
            
            # Get existing video links from database
            existing_links = set(PieceOfContent.objects.filter(
                content_type=ContentType.TIKTOK
            ).values_list('link', flat=True))
            
            # Process videos until we reach max_videos or run out of new ones
            for video in user.videos:
                if len(videos) >= max_videos:
                    break
                    
                video_link = f"https://www.tiktok.com/@{username}/video/{video.id}"
                
                # Skip if video already exists in database
                if video_link in existing_links:
                    continue
                
                videos.append({
                    'link': video_link,
                    'likes': video.stats.digg_count,
                    'views': video.stats.play_count,
                    'description': video.desc,
                    'created_at': video.create_time
                })
            
            return videos
            
    except Exception as e:
        # Log the error and return empty list
        print(f"Error fetching TikTok videos: {str(e)}")
        return []
