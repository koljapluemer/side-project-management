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
    """Ensure the output directory exists, create it if it doesn't."""
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_PATH}")

def get_github_repos():
    """Fetch all repositories owned by the authenticated user using PyGithub."""
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    
    print("Fetching repositories...")
    # Only get repos where the user is the owner
    all_repos = [repo for repo in user.get_repos() if repo.owner.login == user.login]
    
    print(f"\nTotal repositories found: {len(all_repos)}")
    print("Repository names:")
    for repo in all_repos:
        print(f"- {repo.name} (private: {repo.private}, archived: {repo.archived}, stars: {repo.stargazers_count})")
    
    return all_repos

def read_note_content(note_path):
    """Read a note file and separate YAML frontmatter from content."""
    if not note_path.exists():
        return None, ""
    
    content = note_path.read_text()
    parts = content.split('---', 2)
    
    if len(parts) < 3:
        return None, content
    
    yaml_content = parts[1].strip()
    rest_content = parts[2].strip()
    
    try:
        yaml_data = yaml.safe_load(yaml_content) if yaml_content else {}
        return yaml_data, rest_content
    except yaml.YAMLError:
        return None, content

def write_note(note_path, yaml_data, content):
    """Write a note with YAML frontmatter and content."""
    yaml_str = yaml.dump(yaml_data, default_flow_style=False)
    note_content = f"---\n{yaml_str}---\n{content}"
    note_path.write_text(note_content)

def update_repo_notes():
    """Update or create notes for all GitHub repositories."""
    repos = get_github_repos()
    
    for repo in repos:
        note_path = OUTPUT_PATH / f"{repo.name}.md"
        
        # Read existing note or create new one
        yaml_data, content = read_note_content(note_path)
        if yaml_data is None:
            yaml_data = {}
        
        # Update YAML data
        yaml_data['is-archived'] = repo.archived
        yaml_data['stars'] = repo.stargazers_count
        
        # Write the note
        write_note(note_path, yaml_data, content)
        print(f"Updated note for {repo.name} (stars: {repo.stargazers_count})")

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN must be set in .env file")
        exit(1)
    
    # Ensure output directory exists
    ensure_output_directory()
    
    update_repo_notes() 