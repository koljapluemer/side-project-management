from django.db import transaction
from cms.models import Project

def delete_all_projects():
    """
    Deletes all Project objects from the database.
    Returns the number of projects deleted.
    """
    with transaction.atomic():
        count = Project.objects.count()
        Project.objects.all().delete()
        return count
