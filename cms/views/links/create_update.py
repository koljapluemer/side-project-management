from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from cms.models import Link, Project
from django import forms

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url', 'project', 'label']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all().order_by('name')
        self.fields['project'].required = False
        self.fields['project'].empty_label = "No Project"

def link_create_update(request, pk=None):
    link = None
    if pk:
        link = get_object_or_404(Link, pk=pk)
    
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('link_list')
    else:
        form = LinkForm(instance=link)
    
    return render(request, 'links/create_update.html', {
        'form': form,
        'link': link,
        'is_update': pk is not None
    })

def link_delete(request, pk):
    link = get_object_or_404(Link, pk=pk)
    if request.method == 'POST':
        link.delete()
        return redirect('link_list')
    return render(request, 'links/delete.html', {'link': link})
