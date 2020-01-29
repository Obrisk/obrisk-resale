from celery import shared_task
from config.celery import app
from django.conf import settings
from obrisk.qa.models import Question


def migrate_qa_tags():
   '''this runs a background task to update the
   old tags in taggit to new ones in qa app'''
    questions = Question.objects.all()
    
    for question in questions :
        old_tag = question.tags
        question.new_tags = old_tag
 



