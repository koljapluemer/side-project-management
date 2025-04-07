import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from github import Github

# Load environment variables
load_dotenv()

# Constants
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OUTPUT_PATH = Path(os.getenv('OUTPUT_PATH', '~/MEGA')).expanduser()

def ensure_output_directory():
    """Ensure the output directory exists."""
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_PATH}")

def create_repo_notes():
    """Create notes for all GitHub repositories."""
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    
    print("Fetching repositories...")
    # Get all repos where user is the owner
    repos = [repo for repo in user.get_repos() if repo.owner.login == user.login]
    
    print(f"\nTotal repositories found: {len(repos)}")
    print("Repository names:")
    for repo in repos:
        print(f"- {repo.name} (private: {repo.private})")
    
    for repo in repos:
        note_path = OUTPUT_PATH / f"{repo.name}.md"
        
        if not note_path.exists():
            print(f"Creating note for {repo.name}")
            
            # Get repository metadata
            yaml_data = {
                'repo': repo.clone_url,
                'description': repo.description or '',
                'website': repo.homepage or '',
                'tags': [topic for topic in repo.get_topics()],
                'open_issues': repo.open_issues_count,
                'closed_issues': repo.get_issues(state='closed').totalCount
            }
            
            # Create note content
            content = f"""---
{yaml.dump(yaml_data, default_flow_style=False)}---

# {repo.name}

{repo.description or ''}

## Details
- **Open Issues**: {repo.open_issues_count}
- **Closed Issues**: {repo.get_issues(state='closed').totalCount}
{f'- **Website**: {repo.homepage}' if repo.homepage else ''}

## Tags
{', '.join([f'#{topic}' for topic in repo.get_topics()]) or 'No tags'}
"""
            
            note_path.write_text(content)
        else:
            print(f"Note already exists for {repo.name}")

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN must be set in .env file")
        exit(1)
    
    ensure_output_directory()
    create_repo_notes()
    print("Done!") 