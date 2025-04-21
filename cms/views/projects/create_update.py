from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from cms.models import Project, ProjectStatus

class ProjectCreateUpdateView(View):
    template_name = 'projects/create_update.html'
    success_url = reverse_lazy('project_list')

    def get(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk) if pk else None
        context = {
            'object': project,
            'status_choices': ProjectStatus.choices,
            'name': project.name if project else '',
            'status': project.status if project else ProjectStatus.UNKNOWN,
            'description': project.description if project else '',
        }
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk) if pk else None
        
        name = request.POST.get('name', '').strip()
        status = request.POST.get('status', ProjectStatus.UNKNOWN)
        description = request.POST.get('description', '').strip()

        # Basic validation
        if not name:
            messages.error(request, 'Project name is required')
            return self.get(request, pk)

        try:
            if project:
                # Update existing project
                project.name = name
                project.status = status
                project.description = description
                project.save()
                messages.success(request, 'Project updated successfully!')
            else:
                # Create new project
                Project.objects.create(
                    name=name,
                    status=status,
                    description=description
                )
                messages.success(request, 'Project created successfully!')
            
            return redirect(self.success_url)
        except Exception as e:
            messages.error(request, f'Error saving project: {str(e)}')
            return self.get(request, pk) 