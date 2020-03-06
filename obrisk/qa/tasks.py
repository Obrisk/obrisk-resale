from celery import shared_task
from obrisk.qa.models import Question


@shared_task
def migrate_qa_tags():
    '''this updates the old tags in taggit to new ones in qa app'''

    questions = Question.objects.all()

    for question in questions:
        tags = question.tags.all()

        for tag in tags:
            question.new_tags.add(str(tag))
        question.save()
