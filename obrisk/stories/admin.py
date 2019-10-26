from django.contrib import admin
from obrisk.stories.models import Stories, StoryImages

admin.site.register(StoryImages)
@admin.register(Stories)
class StorieseAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'reply')
    list_filter = ('timestamp', 'reply')


