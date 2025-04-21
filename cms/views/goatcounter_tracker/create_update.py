from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from cms.models import Project, GoatcounterTracker

class GoatcounterTrackerCreateView(CreateView):
    model = GoatcounterTracker
    template_name = 'goatcounter_tracker/create_update.html'
    fields = ['goatcounter_id', 'api_key']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        context['is_create'] = True
        return context
    
    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        form.instance.project = project
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['project_pk']})

class GoatcounterTrackerUpdateView(UpdateView):
    model = GoatcounterTracker
    template_name = 'goatcounter_tracker/create_update.html'
    fields = ['goatcounter_id', 'api_key']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project
        context['is_create'] = False
        return context
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.pk})
