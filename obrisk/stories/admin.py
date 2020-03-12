from django.contrib import admin
from obrisk.stories.models import Stories, StoryImages, StoryTags



admin.site.register(StoryImages)
admin.site.register(StoryTags)

@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'reply')
    list_filter = ('timestamp', 'reply')
    readonly_fields = ('slug',)
