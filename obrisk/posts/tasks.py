from celery import shared_task
from obrisk.posts.models import Post


@shared_task
def migrate_posts_tags():
    '''this updates the old tags in taggit to new ones in posts app'''

    posts = Post.objects.all()
    for post in posts:
        tags = post.tags.all()
        for tag in tags:
            post.new_tags.add(tag)
        post.save()


