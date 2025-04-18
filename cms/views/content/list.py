from django.views.generic import ListView
from cms.models import PieceOfContent

class ContentListView(ListView):
    model = PieceOfContent
    template_name = 'content/list.html'
    context_object_name = 'content_list'
    paginate_by = 100
    ordering = ['-created_at']  # Most recent first
