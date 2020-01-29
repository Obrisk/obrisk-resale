from celery import shared_task
from config.celery import app
from obrisk.users.models import User
from django.conf import settings
from obrisk.stories.models import Stories

@app.task
def migrate_stories_tags():
   '''this runs a background task to update the
   old tags in taggit to new ones in stories app'''
    stories = Stories.objects.all()
    
    for story in stories:
        old_tag = story.tags
        story.new_tags = old_tag


