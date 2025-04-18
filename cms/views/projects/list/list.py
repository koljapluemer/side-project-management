from django.views.generic import ListView
from cms.models import Project

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list/list.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        return Project.objects.all().order_by('name')
