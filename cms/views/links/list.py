from django.views.generic import ListView
from cms.models import Link

class LinkListView(ListView):
    model = Link
    template_name = 'links/list.html'
    context_object_name = 'links'
    
    def get_queryset(self):
        return Link.objects.all().order_by('?')
