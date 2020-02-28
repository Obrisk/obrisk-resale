from django.shortcuts import redirect
from obrisk.posts.tasks import migrate_posts_tags
from obrisk.qa.tasks import migrate_qa_tags
from obrisk.classifieds.tasks import migrate_classifieds_tags
from obrisk.stories.tasks import migrate_stories_tags


def migrate_all_tags(request):
    ''' A function to perform all background tasks to migrate tags'''

    migrate_classifieds_tags.delay()
    migrate_posts_tags.delay()
    migrate_qa_tags.delay()
    migrate_stories_tags.delay()

    return redirect("stories:list")
