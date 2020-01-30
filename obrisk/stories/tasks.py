from celery import shared_task
from obrisk.stories.models import Stories


@shared_task
def migrate_stories_tags():
   '''this runs a background task to update the
   old tags in taggit to new ones in stories app'''
    stories = Stories.objects.all()
    
    for story in stories:
        story.new_tags = story.tags
        


