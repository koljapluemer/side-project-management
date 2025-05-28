import os
from datetime import datetime
from django.utils import timezone
from cms.models import Project, Folder, Settings

def sync_local_folders(base_path):
    """
    Sync local folders with Django models by creating Projects and Folders.
    Also creates corresponding markdown files in the Obsidian projects folder.
    
    Args:
        base_path (str): The base path to scan for folders
    """
    if not os.path.exists(base_path):
        raise ValueError(f"Base path {base_path} does not exist")
    
    # Get settings for Obsidian folder
    settings = Settings.objects.first()
    if not settings or not settings.obsidian_projects_folder:
        raise ValueError("Obsidian projects folder not configured in settings")
    
    if not os.path.exists(settings.obsidian_projects_folder):
        raise ValueError(f"Obsidian projects folder {settings.obsidian_projects_folder} does not exist")
    
    # Get all directories in the base path
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        
        # Skip if not a directory
        if not os.path.isdir(folder_path):
            continue
            
        # Skip hidden directories
        if folder_name.startswith('.'):
            continue
            
        # Get the last modification time of the folder
        last_modified = datetime.fromtimestamp(os.path.getmtime(folder_path))
        last_modified = timezone.make_aware(last_modified)
        
        # Create or update Project
        project, created = Project.objects.get_or_create(
            name=folder_name,
            defaults={
                'auto_generated': True,
            }
        )
        
        # Create or update Folder
        folder, created = Folder.objects.get_or_create(
            name=folder_name,
            project=project,
            defaults={
                'metadata_last_checked_at': timezone.now(),
                'last_file_change': last_modified,
                'still_exists': True
            }
        )
        
        # Update existing folder if it exists
        if not created:
            folder.metadata_last_checked_at = timezone.now()
            folder.last_file_change = last_modified
            folder.still_exists = True
            folder.save()
            
        # Create markdown file in Obsidian folder if it doesn't exist
        obsidian_file_path = os.path.join(settings.obsidian_projects_folder, f"{folder_name}.md")
        if not os.path.exists(obsidian_file_path):
            open(obsidian_file_path, 'w').close()
