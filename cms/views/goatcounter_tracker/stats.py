from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from cms.models import GoatcounterTracker
from cms.utils.get_goatcounter_stats import get_goatcounter_stats

def update_goatcounter_stats(request, project_pk, tracker_pk):
    """Update GoatCounter stats for a specific tracker."""
    tracker = get_object_or_404(GoatcounterTracker, pk=tracker_pk, project_id=project_pk)
    
    stats = get_goatcounter_stats(tracker.goatcounter_id, tracker.api_key)
    
    if stats:
        return JsonResponse({
            'status': 'success',
            'message': 'Stats updated successfully',
            'stats': stats
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to update stats'
        }, status=400) 