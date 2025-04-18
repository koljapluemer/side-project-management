from django.core.management.base import BaseCommand
from cms.utils.sync_local_folders import sync_local_folders
from cms.models import Settings

class Command(BaseCommand):
    help = 'Sync local folders with Django models by creating Projects and Folders'

    def handle(self, *args, **options):
        try:
            settings = Settings.objects.first()
            if not settings:
                self.stdout.write(self.style.ERROR('No settings found. Please create a Settings object first.'))
                return
                
            if not settings.local_projects_folder:
                self.stdout.write(self.style.ERROR('No local_projects_folder set in Settings.'))
                return
                
            self.stdout.write(f'Syncing folders from {settings.local_projects_folder}...')
            sync_local_folders(settings.local_projects_folder)
            self.stdout.write(self.style.SUCCESS('Successfully synced local folders'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error syncing folders: {str(e)}')) 