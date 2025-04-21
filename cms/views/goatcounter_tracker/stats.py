from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from cms.models import GoatcounterTracker
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