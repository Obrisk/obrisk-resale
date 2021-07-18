import time
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from celery import shared_task
from obrisk.classifieds.models import Classified, ClassifiedTags


TAGS_TIMEOUT = getattr(
        settings,
        'TAGS_CACHE_TIMEOUT',
        DEFAULT_TIMEOUT
    )

def set_popular_tags():
    popular_tags = Classified.objects.get_active(
            ).get_counted_tags()[:10]

    cache.set('popular_tags_mb',
                list(popular_tags), timeout=TAGS_TIMEOUT
            )

    return HttpResponse(
            "Successfully sorted the popular tags!",
            content_type='text/plain')



@shared_task
def migrate_classifieds_tags():
    '''this function is to update the
    old tags in taggit to new ones in classfieds app'''

    classifieds = Classified.objects.all()
    for classified in classifieds:
        tags = classified.tags.all()
        for tag in tags:
            classified.new_tags.add(str(tag))
        classified.save()


@shared_task
def update_classified_tags():
    set_popular_tags()


@shared_task
def add_tags(item_id):
    time.sleep(5)
    classified = Classified.objects.get(id=item_id)
    tags = ClassifiedTags.objects.values_list('slug', flat=True)

    for title in classified.title.split():
        if title.lower() in tags:
            classified.tags.add(title)
    for det in classified.details.split():
        if det.lower() in tags:
            classified.tags.add(det)

    classified.save()
