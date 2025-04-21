from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from cms.models import GoatcounterTracker, PageViewDay
from cms.utils.get_goatcounter_stats import get_goatcounter_stats

@require_POST
def update_goatcounter_stats(request, project_pk, tracker_pk):
    """Update GoatCounter stats for a specific tracker."""
    try:
        tracker = get_object_or_404(GoatcounterTracker, pk=tracker_pk, project_id=project_pk)
        stats = get_goatcounter_stats(tracker.goatcounter_id, tracker.api_key, tracker.project)
        
        if stats:
            return JsonResponse({
                'status': 'success',
                'stats': stats
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to fetch stats from GoatCounter'
            }, status=500)
    except GoatcounterTracker.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Tracker not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def get_chart_data(request, project_pk, tracker_pk):
    """Get page view data for the last 14 days."""
    try:
        tracker = get_object_or_404(GoatcounterTracker, pk=tracker_pk, project_id=project_pk)
        
        # Calculate date range
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=13)  # 14 days total
        
        # Get page views for the date range
        page_views = PageViewDay.objects.filter(
            project=tracker.project,
            date__range=[start_date, end_date]
        ).order_by('date')
        
        # Create lists for dates and views
        dates = []
        views = []
        
        # Initialize all dates in range
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime('%Y-%m-%d'))
            views.append(0)  # Default to 0 views
            current_date += timedelta(days=1)
        
        # Update views for dates that have data
        for pv in page_views:
            date_str = pv.date.strftime('%Y-%m-%d')
            if date_str in dates:
                index = dates.index(date_str)
                views[index] = pv.views
        
        return JsonResponse({
            'dates': dates,
            'views': views
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500) 