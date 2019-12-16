from celery import shared_task
from obrisk.classifieds.views import set_popular_tags

@shared_task
def update_classified_tags():
    set_popular_tags()