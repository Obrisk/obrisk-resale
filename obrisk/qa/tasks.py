from celery import shared_task
from obrisk.qa.models import Question


@shared_task
def migrate_qa_tags():
   '''this runs a background task to update the
   old tags in taggit to new ones in qa app'''
    questions = Question.objects.all()
    
    for question in questions :
       question.new_tags = question.tags
 



