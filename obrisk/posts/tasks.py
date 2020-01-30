from celery import shared_task
from obrisk.posts.models import Post


@shared_task
def migrate_posts_tags():
   '''this runs a background task to update the
   old tags in taggit to new ones in posts app'''

    posts = Post.objects.all()
    
    for post  in posts:
        post.new_tags = post.tags
        


