import requests
from django.utils import timezone
from cms.models import Project, Repository, Settings
from django.db import transaction
import re


def get_all_repos(headers):
    """
    Fetches all repositories from GitHub using pagination.
    Returns a list of all repository data.
    """
    all_repos = []
    url = 'https://api.github.com/user/repos?per_page=100'
    
    # First get the authenticated user's login name
    user_response = requests.get('https://api.github.com/user', headers=headers)
    user_response.raise_for_status()
    user_login = user_response.json()['login']
    
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Only include repos where the owner's login matches the authenticated user
        for repo in response.json():
            if repo['owner']['login'] == user_login:
                all_repos.append(repo)
        
        # Check for next page in Link header
        link_header = response.headers.get('Link')
        if not link_header:
            break
            
        # Parse Link header to find next page URL
        # GitHub Link header format: <url>; rel="next", <url>; rel="last" ...
        url = None
        for link in link_header.split(','):
            if 'rel="next"' in link:
                url_match = re.search(r'<(.+?)>', link)
                if url_match:
                    url = url_match.group(1)
                break
    
    return all_repos

def sync_github_repositories():
    """
    Syncs GitHub repositories with the Project model.
    Creates new Projects for repositories that don't exist and updates existing ones.
    Only includes repositories directly owned by the authenticated user.
    """
    settings = Settings.objects.first()
    if not settings or not settings.github_token:
        raise ValueError("GitHub token not configured in settings")

    headers = {
        'Authorization': f'token {settings.github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get all repositories from GitHub using pagination
    repos = get_all_repos(headers)

    with transaction.atomic():
        for repo_data in repos:
            # Create or update Repository
            repo, created = Repository.objects.update_or_create(
                link=repo_data['html_url'],
                defaults={
                    'name': repo_data['name'],
                    'description': repo_data['description'],
                    'stars': repo_data['stargazers_count'],
                    'is_archived': repo_data['archived'],
                    'is_private': repo_data['private'],
                    'metadata_last_checked_at': timezone.now(),
                    'last_commit_at': repo_data['pushed_at'],
                    'linked_website': repo_data['homepage'] if repo_data['homepage'] else None,
                }
            )

            # Create or update Project if it doesn't exist
            if not repo.project:
                project, _ = Project.objects.get_or_create(
                    name=repo.name,
                    defaults={
                        'description': repo.description,
                        'auto_generated': True,
                    }
                )
                repo.project = project
                repo.save()

    return len(repos)
