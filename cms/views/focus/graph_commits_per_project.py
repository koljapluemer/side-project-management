from django.shortcuts import render
from django.http import JsonResponse
from cms.utils.get_nr_of_commits_per_week_and_project import get_nr_of_commits_per_week_and_project
import json
import colorsys


def graph_commits_per_project_view(request):
    """
    View to display a stacked area chart showing commits per project over the last 10 weeks.
    """
    try:
        data = get_nr_of_commits_per_week_and_project()
        return render(request, 'focus/graph_commits_per_project.html', {
            'weeks': data['weeks'],
            'week_numbers': data['week_numbers'],
            'projects': data['projects'],
            'projects_per_week': data['projects_per_week']
        })
    except Exception as e:
        # For personal local software, just raise the error
        raise e


def generate_distinct_colors(n):
    """
    Generate n distinct colors using HSV color space to avoid collisions.
    """
    colors = []
    for i in range(n):
        # Use golden ratio to distribute colors evenly in HSV space
        hue = (i * 0.618033988749895) % 1.0
        saturation = 0.7 + (i % 3) * 0.1  # Vary saturation slightly
        value = 0.8 + (i % 2) * 0.1       # Vary brightness slightly
        
        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        
        # Convert to hex
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        colors.append(hex_color)
    
    return colors


def graph_commits_per_project_data(request):
    """
    API endpoint to return commit data as JSON for Chart.js.
    """
    try:
        data = get_nr_of_commits_per_week_and_project()
        
        # Format data for Chart.js stacked area chart
        chart_data = {
            'labels': data['week_numbers'],
            'datasets': []
        }
        
        # Generate distinct colors for projects
        project_names = list(data['projects'].keys())
        colors = generate_distinct_colors(len(project_names))
        
        for i, (project_name, commit_counts) in enumerate(data['projects'].items()):
            color = colors[i]
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


def graph_projects_per_week_data(request):
    """
    API endpoint to return projects per week data as JSON for Chart.js bar chart.
    """
    try:
        data = get_nr_of_commits_per_week_and_project()
        
        chart_data = {
            'labels': data['week_numbers'],
            'datasets': [{
                'label': 'Number of Projects',
                'data': data['projects_per_week'],
                'backgroundColor': '#36A2EB',
                'borderColor': '#2693E6',
                'borderWidth': 1
            }]
        }
        
        return JsonResponse(chart_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
