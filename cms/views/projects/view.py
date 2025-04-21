from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from cms.models import Project, GoatcounterTracker, PageViewDay
from django.utils import timezone
from datetime import timedelta

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/show.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get the GoatCounter tracker if it exists
        try:
            goatcounter_tracker = GoatcounterTracker.objects.get(project=project)
            context['goatcounter_tracker'] = goatcounter_tracker
        except GoatcounterTracker.DoesNotExist:
            context['goatcounter_tracker'] = None
            
        # Check if project has any deployments
        context['has_deployments'] = project.deployment_set.exists()

        # Add chart data if tracker exists
        if context['goatcounter_tracker']:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=13)  # 14 days total
            
            # Get page views for the date range
            page_views = PageViewDay.objects.filter(
                project=project,
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
            
            context['chart_data'] = {
                'dates': dates,
                'views': views
            }
        
        return context
