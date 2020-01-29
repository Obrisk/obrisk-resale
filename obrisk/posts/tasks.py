from celery import shared_task
from config.celery import app
from django.conf import settings
from obrisk.posts.models import Post


@app.task
def migrate_posts_tags():
   '''this runs a background task to update the
   old tags in taggit to new ones in posts app'''

    posts = Post.objects.all()
    
    for post  in posts:
        old_tag = post.tags
        post.new_tags = old_tag


