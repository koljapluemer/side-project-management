from django.shortcuts import render, redirect
from django.contrib import messages
from cms.models import Goal

def goals_view(request):
    # Get or create the singleton goal instance
    goal, created = Goal.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        # Update TikTok goals
        goal.tiktok_goal_type = request.POST.get('tiktok_goal_type', 'none')
        goal.tiktok_streak_goal = request.POST.get('tiktok_streak_goal', 0)
        goal.tiktok_milestone_goal = request.POST.get('tiktok_milestone_goal', 0)
        
        # Update Twitter goals
        goal.twitter_goal_type = request.POST.get('twitter_goal_type', 'none')
        goal.twitter_streak_goal = request.POST.get('twitter_streak_goal', 0)
        goal.twitter_milestone_goal = request.POST.get('twitter_milestone_goal', 0)
        
        # Update Reddit goals
        goal.reddit_goal_type = request.POST.get('reddit_goal_type', 'none')
        goal.reddit_streak_goal = request.POST.get('reddit_streak_goal', 0)
        goal.reddit_milestone_goal = request.POST.get('reddit_milestone_goal', 0)
        
        goal.save()
        messages.success(request, 'Goals updated successfully!')
        return redirect('goals')
    
    return render(request, 'goals/view.html', {
        'goal': goal
    })
