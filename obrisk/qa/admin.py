from django.contrib import admin
from obrisk.qa.models import Question, Answer, QaTags


admin.site.register(QaTags)
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')
    list_filter = ('user', 'status', 'timestamp')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'timestamp')
    list_filter = ('timestamp', 'votes')
    search_fields = ('user', 'content')
