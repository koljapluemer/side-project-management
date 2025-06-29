import subprocess
import os
from datetime import datetime, timedelta
from django.utils import timezone
from cms.models import Settings, Project, Folder


def get_nr_of_commits_per_week_and_project():
    """
    Get the number of commits per week and project for the last 10 weeks.
    Uses local Git repositories instead of GitHub API.
    Returns a dictionary with weeks as keys and project commit counts as values.
    """
    settings = Settings.objects.first()
    if not settings or not settings.local_projects_folder:
        raise ValueError("Local projects folder not configured in settings")
    
    if not os.path.exists(settings.local_projects_folder):
        raise ValueError(f"Local projects folder {settings.local_projects_folder} does not exist")

    # Calculate date range (last 10 weeks)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(weeks=10)
    
    # Initialize data structure with actual week numbers of the year
    weeks = []
    week_numbers = []
    current_date = start_date
    while current_date <= end_date:
        weeks.append(current_date.strftime('%Y-%m-%d'))
        # Get the ISO week number of the year
        week_num = current_date.isocalendar()[1]
        week_numbers.append(f"Week {week_num}")
        current_date += timedelta(weeks=1)
    
    project_commits = {}
    
    # Get all directories in the local projects folder
    for folder_name in os.listdir(settings.local_projects_folder):
        folder_path = os.path.join(settings.local_projects_folder, folder_name)
        
        # Skip if not a directory
        if not os.path.isdir(folder_path):
            continue
            
        # Skip hidden directories
        if folder_name.startswith('.'):
            continue
        
        # Check if this is a Git repository
        git_dir = os.path.join(folder_path, '.git')
        if not os.path.exists(git_dir):
            continue
        
        # Get commits for this repository
        commits = get_repository_commits(folder_path, start_date, end_date)
        
        if commits:  # Only include projects with commits
            project_commits[folder_name] = commits
    
    # Calculate number of different projects per week
    projects_per_week = []
    for week_idx in range(len(weeks)):
        week_project_count = 0
        for project_name, commit_counts in project_commits.items():
            if commit_counts[week_idx] > 0:
                week_project_count += 1
        projects_per_week.append(week_project_count)
    
    return {
        'weeks': weeks,
        'week_numbers': week_numbers,
        'projects': project_commits,
        'projects_per_week': projects_per_week
    }


def get_repository_commits(repo_path, start_date, end_date):
    """
    Get commits for a specific local repository within the date range.
    Returns a list of commit counts per week.
    """
    # Calculate weeks
    weeks = []
    current_date = start_date
    while current_date <= end_date:
        weeks.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(weeks=1)
    
    # Initialize commit counts for each week
    commit_counts = [0] * len(weeks)
    
    try:
        # Use git log to get commits within the date range
        # Format: --pretty=format:"%H %ad" --date=short
        cmd = [
            'git', 'log',
            '--pretty=format:%ad',
            '--date=short',
            f'--since={start_date.isoformat()}',
            f'--until={end_date.isoformat()}',
            '--all'  # Include all branches
        ]
        
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        if result.returncode != 0:
            print(f"Git command failed for {repo_path}: {result.stderr}")
            return []
        
        # Parse commit dates
        for line in result.stdout.strip().split('\n'):
            if not line.strip():
                continue
                
            try:
                commit_date = datetime.strptime(line.strip(), '%Y-%m-%d').date()
                
                # Find which week this commit belongs to
                for i, week_start in enumerate(weeks):
                    week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
                    week_end_date = week_start_date + timedelta(weeks=1)
                    
                    if week_start_date <= commit_date < week_end_date:
                        commit_counts[i] += 1
                        break
                        
            except ValueError:
                # Skip invalid date formats
                continue
                    
    except subprocess.TimeoutExpired:
        print(f"Git command timed out for {repo_path}")
        return []
    except Exception as e:
        print(f"Error getting commits for {repo_path}: {e}")
        return []
    
    return commit_counts
