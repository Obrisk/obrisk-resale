from celery import shared_task
from config.celery import app
from django.conf import settings
from obrisk.classifieds.models import Classified
from obrisk.classifieds.views import set_popular_tags

@app.task
def migrate_classifieds_tags():
   '''this runs a background task to update the
   old tags in taggit to new ones in classfieds app'''

    classifieds = Classified.objects.all()
        
    for classified in classified:
        old_tag = classified.tags
        classified.new_tags = old_tag

@shared_task
def update_classified_tags():
    set_popular_tags()

