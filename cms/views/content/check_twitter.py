from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from cms.models import PieceOfContent, Settings, ContentType
from cms.utils.get_tweets_from_account import get_new_tweets_from_account

def check_twitter_view(request):
    """
    View to check for new tweets from the configured Twitter account.
    """
    settings_obj = Settings.objects.first()
    if not settings_obj or not settings_obj.twitter_account_name:
        messages.error(request, "Twitter account name not configured in settings")
        return redirect('settings')
    
    # Strip @ from username if present
    username = settings_obj.twitter_account_name.lstrip('@')
    
    # Fetch new tweets
    new_tweets = get_new_tweets_from_account(username)
    
    if not new_tweets:
        messages.info(request, "No new tweets found")
        return redirect('content_list')
    
    # Save new tweets to database
    saved_count = 0
    for tweet in new_tweets:
        try:
            PieceOfContent.objects.create(
                content_type=ContentType.TWEET,
                link=tweet['link'],
                likes=tweet['likes'],
                views=tweet['views'],
                posted_at=tweet['posted_at']
            )
            saved_count += 1
        except Exception as e:
            messages.error(request, f"Error saving tweet: {str(e)}")
            continue
    
    if saved_count > 0:
        messages.success(request, f"Added {saved_count} new tweets")
    else:
        messages.warning(request, "No new tweets were added")
    
    return redirect('content_list')
