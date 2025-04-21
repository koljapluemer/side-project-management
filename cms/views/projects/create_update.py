from django.shortcuts import render, redirect
from django.contrib import messages
from cms.models import Project

def project_create_update(request, pk=None):
    project = None
    if pk:
        project = Project.objects.get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if not name:
            messages.error(request, 'Project name is required')
            return render(request, 'projects/create_update.html', {
                'object': project,
                'name': name,
                'description': description,
            })

        if project:
            project.name = name
            project.description = description
            project.save()
            messages.success(request, 'Project updated successfully')
        else:
            Project.objects.create(
                name=name,
                description=description,
            )
            messages.success(request, 'Project created successfully')

        return redirect('project_list')

    return render(request, 'projects/create_update.html', {
        'object': project,
        'name': project.name if project else '',
        'description': project.description if project else '',
    }) 