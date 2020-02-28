from celery import shared_task
from obrisk.classifieds.models import Classified
from obrisk.classifieds.views import set_popular_tags


@shared_task
def migrate_classifieds_tags():
    '''this function is to update the
    old tags in taggit to new ones in classfieds app'''

    classifieds = Classified.objects.all()
    for classified in classifieds:
        classified.new_tags = classified.tags.all()
        classified.save()


@shared_task
def update_classified_tags():
    set_popular_tags()
