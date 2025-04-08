import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Constants
OUTPUT_PATH = Path(os.getenv('OUTPUT_PATH', '~/MEGA')).expanduser()
GOATCOUNTER_KEY = os.getenv('GOATCOUNTER_KEY', '')  # Your GoatCounter site key

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

def get_goatcounter_link(website_url):
    """Generate GoatCounter link for a website URL."""
    if not website_url:
        return ''
    
    # Extract domain from URL
    domain = urlparse(website_url).netloc
    if not domain:
        return ''
    
    return f"https://{GOATCOUNTER_KEY}.goatcounter.com/count?p={domain}"

def add_goatcounter_props():
    """Add empty GoatCounter properties to notes with website URLs."""
    # Get all markdown files in the output directory
    for note_path in OUTPUT_PATH.glob('*.md'):
        print(f"\nProcessing {note_path.name}...")
        
        # Read existing note
        yaml_data, content = read_note_content(note_path)
        if yaml_data is None:
            print(f"  Skipping {note_path.name} - no valid YAML frontmatter")
            continue
            
        # Check if this note has a website
        if 'website' not in yaml_data or not yaml_data['website']:
            print(f"  Skipping {note_path.name} - no website URL")
            continue
            
        # Skip if GoatCounter props already exist
        if 'goatcounter-link' in yaml_data and 'goatcounter-key' in yaml_data:
            print(f"  Skipping {note_path.name} - GoatCounter props already exist")
            continue
            
        # Add empty GoatCounter properties
        yaml_data.update({
            'goatcounter-link': '',
            'goatcounter-key': ''
        })
        
        # Write the note
        write_note(note_path, yaml_data, content)
        print(f"  Added empty GoatCounter props for {note_path.name}")

if __name__ == "__main__":
    add_goatcounter_props()
