from django.shortcuts import render
from django.http import JsonResponse
from cms.utils.get_nr_of_commits_per_week_and_project import get_nr_of_commits_per_week_and_project
import json


def graph_commits_per_project_view(request):
    """
    View to display a stacked area chart showing commits per project over the last 10 weeks.
    """
    try:
        data = get_nr_of_commits_per_week_and_project()
        return render(request, 'focus/graph_commits_per_project.html', {
            'weeks': data['weeks'],
            'projects': data['projects']
        })
    except Exception as e:
        # For personal local software, just raise the error
        raise e


def graph_commits_per_project_data(request):
    """
    API endpoint to return commit data as JSON for Chart.js.
    """
    try:
        data = get_nr_of_commits_per_week_and_project()
        
        # Format data for Chart.js stacked area chart
        chart_data = {
            'labels': data['weeks'],
            'datasets': []
        }
        
        # Generate colors for projects
        colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ]
        
        for i, (project_name, commit_counts) in enumerate(data['projects'].items()):
            color = colors[i % len(colors)]
            chart_data['datasets'].append({
                'label': project_name,
                'data': commit_counts,
                'backgroundColor': color + '40',  # 40 = 25% opacity
                'borderColor': color,
                'borderWidth': 2,
                'fill': True,
                'stack': 'Stack 0',
                'tension': 0.4
            })
        
        return JsonResponse(chart_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
