from obrisk.posts.models import Post


def migrate_posts_tags():
    '''this updates the old tags in taggit to new ones in posts app'''

    posts = Post.objects.all()
    for post  in posts:
        post.new_tags = post.tags.all()
