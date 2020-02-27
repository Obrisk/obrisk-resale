from obrisk.qa.models import Question


def migrate_qa_tags():
    '''this updates the old tags in taggit to new ones in qa app'''

    questions = Question.objects.all()
    
    for question in questions :
       question.new_tags = question.tags.all()
