from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from cms.models import PieceOfContent, ContentType, GoatcounterTracker, PageViewDay
from cms.utils.get_goatcounter_stats import get_goatcounter_stats
from cms.utils.streaks import calculate_streak_progress

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the last 30 days
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Get all content in the last 30 days for streak visualization
        recent_content = PieceOfContent.objects.filter(
            posted_at__gte=start_date,
            posted_at__lte=end_date
        )
        
        # Get total counts for each platform (all time)
        total_tiktok = PieceOfContent.objects.filter(content_type=ContentType.TIKTOK.value).count()
        total_twitter = PieceOfContent.objects.filter(content_type=ContentType.TWEET.value).count()
        total_reddit = PieceOfContent.objects.filter(content_type=ContentType.REDDIT_POST.value).count()
        
        # Create a dictionary to store daily content counts
        days = {}
        current_date = start_date
        while current_date <= end_date:
            days[current_date.date()] = {
                'tiktok': False,
                'twitter': False,
                'reddit': False
            }
            current_date += timedelta(days=1)
        
        # Mark days with content
        for content in recent_content:
            content_date = content.posted_at.date()
            if content_date in days:
                if content.content_type == ContentType.TIKTOK.value:
                    days[content_date]['tiktok'] = True
                elif content.content_type == ContentType.TWEET.value:
                    days[content_date]['twitter'] = True
                elif content.content_type == ContentType.REDDIT_POST.value:
                    days[content_date]['reddit'] = True
        
        # Convert to list for template
        streak_data = [
            {
                'date': date,
                'tiktok': data['tiktok'],
                'twitter': data['twitter'],
                'reddit': data['reddit']
            }
            for date, data in sorted(days.items())
        ]
        
        # Calculate streak progress for each platform
        tiktok_progress = calculate_streak_progress(ContentType.TIKTOK.value, streak_data)
        twitter_progress = calculate_streak_progress(ContentType.TWEET.value, streak_data)
        reddit_progress = calculate_streak_progress(ContentType.REDDIT_POST.value, streak_data)
        
        # Update milestone progress with total counts
        tiktok_progress['milestone_status']['progress'] = total_tiktok
        twitter_progress['milestone_status']['progress'] = total_twitter
        reddit_progress['milestone_status']['progress'] = total_reddit
        
        # Get GoatCounter stats for all projects
        goatcounter_projects = []
        trackers = GoatcounterTracker.objects.all()
        
        for tracker in trackers:
            # Get last 14 days of page views for this project
            page_views = PageViewDay.objects.filter(
                project=tracker.project,
                date__gte=end_date.date() - timedelta(days=14),
                date__lte=end_date.date()
            ).order_by('date')
            
            # Prepare data for the chart
            dates = [pv.date.strftime('%Y-%m-%d') for pv in page_views]
            views = [pv.views for pv in page_views]
            
            goatcounter_projects.append({
                'project': tracker.project,
                'goatcounter_id': tracker.goatcounter_id,
                'chart_data': {
                    'dates': dates,
                    'views': views
                }
            })
        
        context['streak_data'] = streak_data
        context['goatcounter_projects'] = goatcounter_projects
        context['tiktok_progress'] = tiktok_progress
        context['twitter_progress'] = twitter_progress
        context['reddit_progress'] = reddit_progress
        return context

@method_decorator(require_POST, name='dispatch')
class UpdateStatsView(TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            # Get all GoatCounter trackers
            trackers = GoatcounterTracker.objects.all()
            
            # Update stats for each tracker
            for tracker in trackers:
                get_goatcounter_stats(
                    goatcounter_id=tracker.goatcounter_id,
                    api_key=tracker.api_key,
                    project=tracker.project
                )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
