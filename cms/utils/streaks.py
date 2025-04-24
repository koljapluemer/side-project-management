from datetime import datetime, timedelta
from django.utils import timezone
from cms.models import PieceOfContent, ContentType, Goal

def calculate_streak_progress(content_type, days_data):
    """
    Calculate streak progress and goal status for a given content type.
    
    Args:
        content_type: The content type to check (TIKTOK, TWEET, or REDDIT_POST)
        days_data: List of dictionaries containing daily content data
    
    Returns:
        Dictionary containing:
        - current_streak: Number of consecutive days with content
        - longest_streak: Longest streak in the period
        - goal_status: Dictionary with goal progress information
        - milestone_status: Dictionary with milestone progress information
    """
    # Get the goal settings
    goal = Goal.objects.first()
    if not goal:
        empty_status = {
            'has_goal': False,
            'goal_type': 'none',
            'progress': 0,
            'target': 0,
            'is_achieved': False
        }
        return {
            'current_streak': 0,
            'longest_streak': 0,
            'goal_status': empty_status.copy(),
            'milestone_status': empty_status.copy()
        }
    
    # Map content types to their corresponding goal attributes
    goal_attr_map = {
        ContentType.TIKTOK.value: 'tiktok',
        ContentType.TWEET.value: 'twitter',
        ContentType.REDDIT_POST.value: 'reddit'
    }
    
    platform = goal_attr_map[content_type]
    
    # Get goal settings for the content type
    goal_type = getattr(goal, f'{platform}_goal_type')
    streak_goal = getattr(goal, f'{platform}_streak_goal')
    milestone_goal = getattr(goal, f'{platform}_milestone_goal')
    
    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    total_posts = 0
    
    for day in reversed(days_data):  # Start from most recent
        has_content = day[platform]
        if has_content:
            temp_streak += 1
            total_posts += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            if current_streak == 0:  # Only set current_streak once
                current_streak = temp_streak
            temp_streak = 0
    
    # If we haven't broken the streak yet, current_streak is temp_streak
    if current_streak == 0:
        current_streak = temp_streak
    
    # Calculate goal progress
    goal_status = {
        'has_goal': goal_type != 'none',
        'goal_type': goal_type,
        'progress': 0,
        'target': 0,
        'is_achieved': False
    }
    
    # Calculate milestone progress
    milestone_status = {
        'has_goal': milestone_goal > 0,
        'progress': total_posts,
        'target': milestone_goal,
        'is_achieved': total_posts >= milestone_goal
    }
    
    if goal_type == 'day_based':
        # For day-based goals, check if we've reached the streak goal
        goal_status['target'] = streak_goal
        goal_status['progress'] = current_streak
        goal_status['is_achieved'] = current_streak >= streak_goal
    elif goal_type == 'week_based':
        # For week-based goals, count posts this week
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        posts_this_week = sum(
            1 for day in days_data 
            if week_start <= day['date'] <= today and day[platform]
        )
        goal_status['target'] = milestone_goal
        goal_status['progress'] = posts_this_week
        goal_status['is_achieved'] = posts_this_week >= milestone_goal
    elif goal_type == 'month_based':
        # For month-based goals, count posts this month
        today = timezone.now().date()
        month_start = today.replace(day=1)
        posts_this_month = sum(
            1 for day in days_data 
            if month_start <= day['date'] <= today and day[platform]
        )
        goal_status['target'] = milestone_goal
        goal_status['progress'] = posts_this_month
        goal_status['is_achieved'] = posts_this_month >= milestone_goal
    
    return {
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'goal_status': goal_status,
        'milestone_status': milestone_status
    }
