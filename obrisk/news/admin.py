from django.contrib import admin
from obrisk.news.models import News


@admin.register(News)
class NewseAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'reply')
    list_filter = ('timestamp', 'reply')
