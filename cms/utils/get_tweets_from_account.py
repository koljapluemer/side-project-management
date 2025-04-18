from typing import List, Dict
import tweepy
from django.utils import timezone
from cms.models import PieceOfContent, ContentType, Settings
from asgiref.sync import sync_to_async
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@sync_to_async
def get_settings():
    return Settings.objects.first()

@sync_to_async
def get_existing_links():
    return set(PieceOfContent.objects.filter(
        content_type=ContentType.TWEET
    ).values_list('link', flat=True))

def get_new_tweets_from_account(account_name: str) -> List[Dict]:
    """
    Fetch new tweets from a Twitter account that haven't been added to the database yet.
    
    Args:
        account_name: Twitter username without the @ symbol
        
    Returns:
        List of dictionaries containing tweet details:
        - link: URL to the tweet
        - likes: Number of likes
        - views: Number of views
        - posted_at: When the tweet was posted
    """
    settings = Settings.objects.first()
    if not settings or not settings.twitter_bearer_token:
        logger.error("Twitter bearer token not configured in settings")
        return []
    
    bearer_token = settings.twitter_bearer_token
    
    try:
        # Initialize Twitter client
        client = tweepy.Client(bearer_token=bearer_token)
        
        # Get user ID from username
        user = client.get_user(username=account_name)
        if not user.data:
            logger.error(f"Could not find Twitter user: {account_name}")
            return []
        
        user_id = user.data.id
        
        # Get existing tweet links from database
        existing_links = set(PieceOfContent.objects.filter(
            content_type=ContentType.TWEET
        ).values_list('link', flat=True))
        
        # Fetch tweets
        tweets = client.get_users_tweets(
            user_id,
            max_results=100,
            tweet_fields=['public_metrics', 'created_at']
        )
        
        if not tweets.data:
            logger.info(f"No tweets found for user: {account_name}")
            return []
        
        new_tweets = []
        for tweet in tweets.data:
            tweet_url = f"https://twitter.com/{account_name}/status/{tweet.id}"
            
            if tweet_url in existing_links:
                continue
                
            new_tweets.append({
                'link': tweet_url,
                'likes': tweet.public_metrics.get('like_count', 0),
                'views': tweet.public_metrics.get('impression_count', 0),
                'posted_at': tweet.created_at
            })
            
        logger.info(f"Found {len(new_tweets)} new tweets for {account_name}")
        return new_tweets
        
    except Exception as e:
        logger.error(f"Error fetching tweets: {str(e)}")
        return []
