from celery import shared_task
from obrisk.stories.models import Stories


@shared_task
def migrate_stories_tags():
    '''this updates the old tags in taggit to new ones in stories app'''

    stories = Stories.objects.all()
    for story in stories:
        tags = story.tags.all()
        for tag in tags:
            story.new_tags.add(str(tag))
        story.save()
