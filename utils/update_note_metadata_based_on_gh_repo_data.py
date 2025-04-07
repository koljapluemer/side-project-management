import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from github import Github
import re

# Load environment variables
load_dotenv()

# Constants
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OUTPUT_PATH = Path(os.getenv('OUTPUT_PATH', '~/MEGA')).expanduser()

def get_repo_from_url(url):
    """Extract owner and repo name from GitHub URL."""
    # Match both https and ssh URLs
    match = re.match(r'https://github.com/([^/]+)/([^/]+)\.git$|git@github.com:([^/]+)/([^/]+)\.git$', url)
    if match:
        # Return the first two groups for https or last two for ssh
        return match.group(1) or match.group(3), match.group(2) or match.group(4)
    return None, None

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

def update_metadata():
    """Update metadata for all repository notes."""
    g = Github(GITHUB_TOKEN)
    
    # Get all markdown files in the output directory
    for note_path in OUTPUT_PATH.glob('*.md'):
        print(f"\nProcessing {note_path.name}...")
        
        # Read existing note
        yaml_data, content = read_note_content(note_path)
        if yaml_data is None:
            print(f"  Skipping {note_path.name} - no valid YAML frontmatter")
            continue
            
        # Check if this is a repo note
        if 'repo' not in yaml_data:
            print(f"  Skipping {note_path.name} - no repo URL")
            continue
            
        # Get repo owner and name
        owner, repo_name = get_repo_from_url(yaml_data['repo'])
        if not owner or not repo_name:
            print(f"  Skipping {note_path.name} - invalid repo URL")
            continue
            
        try:
            # Get repo data from GitHub
            repo = g.get_repo(f"{owner}/{repo_name}")
            
            # Update YAML data
            yaml_data['is-archived'] = repo.archived
            yaml_data['stars'] = repo.stargazers_count
            
            # Write the note
            write_note(note_path, yaml_data, content)
            print(f"  Updated metadata for {repo_name} (stars: {repo.stargazers_count}, archived: {repo.archived})")
            
        except Exception as e:
            print(f"  Error updating {note_path.name}: {str(e)}")

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN must be set in .env file")
        exit(1)
    
    update_metadata() 