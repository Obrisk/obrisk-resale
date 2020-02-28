from django.contrib import admin
from obrisk.posts.models import Post, Comment, PostTags
admin.site.register(PostTags)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')
    list_filter = ('user', 'status', 'timestamp')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('user', 'body')
