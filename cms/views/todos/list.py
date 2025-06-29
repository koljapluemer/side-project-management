from django.views.generic import TemplateView
from cms.models import Repository, Link
import random

class TodoListView(TemplateView):
    template_name = 'todos/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get repositories with linked_website but no associated links
        repositories_without_links = []
        for repo in Repository.objects.filter(linked_website__isnull=False).exclude(linked_website=''):
            if not Link.objects.filter(project=repo.project).exists():
                repositories_without_links.append({
                    'type': 'repository',
                    'title': f'Add link for {repo.name}',
                    'description': f'Repository {repo.name} has a website ({repo.linked_website}) but no associated link',
                    'url': repo.linked_website,
                    'project': repo.project
                })

        # Randomize the order of todos
        random.shuffle(repositories_without_links)
        context['todos'] = repositories_without_links
        return context 