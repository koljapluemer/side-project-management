from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from cms.models import Project, GoatcounterTracker

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
            
        return context
