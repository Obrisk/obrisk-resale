from obrisk.stories.models import Stories


def migrate_stories_tags():
    '''this updates the old tags in taggit to new ones in stories app'''
   
    stories = Stories.objects.all()
    for story in stories:
        story.new_tags = story.tags.all()
