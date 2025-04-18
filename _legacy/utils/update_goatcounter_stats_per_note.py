import os
import yaml
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Constants
OUTPUT_PATH = Path(os.getenv('OUTPUT_PATH', '~/MEGA')).expanduser()

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

def get_goatcounter_stats(goatcounter_key, goatcounter_link):
    """Fetch stats from GoatCounter API."""
    if not goatcounter_key or not goatcounter_link:
        return None, None
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {goatcounter_key}'
    }
    
    url = f'https://{goatcounter_link}.goatcounter.com/api/v0/stats/hits'
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch stats: HTTP {response.status_code}")
            return None, None
            
        data = response.json()
        
        views_today = 0
        views_week = 0
        
        if data.get('hits'):
            stats = data['hits'][0]['stats']
            if stats:
                views_today = stats[-1]['daily']
                views_week = sum(day['daily'] for day in stats)
        
        return views_today, views_week
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch stats: Network error")
        return None, None
    except Exception as e:
        print(f"Failed to fetch stats: Unexpected error")
        return None, None

def update_goatcounter_stats():
    """Update GoatCounter stats for all notes with valid GoatCounter properties."""
    # Get all markdown files in the output directory
    for note_path in OUTPUT_PATH.glob('*.md'):
        # Read existing note
        yaml_data, content = read_note_content(note_path)
        if yaml_data is None:
            continue
            
        # Check if this note has valid GoatCounter properties
        if 'goatcounter-key' not in yaml_data or 'goatcounter-link' not in yaml_data:
            continue
            
        goatcounter_key = yaml_data['goatcounter-key']
        goatcounter_link = yaml_data['goatcounter-link']
        
        if not goatcounter_key or not goatcounter_link:
            continue
            
        # Get stats from GoatCounter
        views_today, views_week = get_goatcounter_stats(goatcounter_key, goatcounter_link)
        if views_today is None or views_week is None:
            print(f"Failed to update {note_path.name}")
            continue
            
        # Update YAML data
        yaml_data.update({
            'views-today': views_today,
            'views-this-week': views_week
        })
        
        # Write the note
        write_note(note_path, yaml_data, content)
        print(f"Updated {note_path.name} (today: {views_today}, week: {views_week})")

if __name__ == "__main__":
    update_goatcounter_stats()
