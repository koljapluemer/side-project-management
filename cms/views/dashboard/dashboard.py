from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from cms.models import PieceOfContent, ContentType

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the last 30 days
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Get all content in the last 30 days
        recent_content = PieceOfContent.objects.filter(
            posted_at__gte=start_date,
            posted_at__lte=end_date
        )
        
        # Create a dictionary to store daily content counts
        days = {}
        current_date = start_date
        while current_date <= end_date:
            days[current_date.date()] = {
                'tiktok': False,
                'tweet': False
            }
            current_date += timedelta(days=1)
        
        # Mark days with content
        for content in recent_content:
            content_date = content.posted_at.date()
            if content_date in days:
                if content.content_type == ContentType.TIKTOK:
                    days[content_date]['tiktok'] = True
                elif content.content_type == ContentType.TWEET:
                    days[content_date]['tweet'] = True
        
        # Convert to list for template
        streak_data = [
            {
                'date': date,
                'tiktok': data['tiktok'],
                'tweet': data['tweet']
            }
            for date, data in sorted(days.items())
        ]
        
        context['streak_data'] = streak_data
        return context
