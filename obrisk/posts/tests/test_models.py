from test_plus.test import TestCase

from obrisk.posts.models import Post


class PostsModelsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
        self.post = Post.objects.create(
            title="A really nice title",
            content="This is a really good content",
            status="P",
            user=self.user,
        )
        self.not_p_post = Post.objects.create(
            title="A really nice to-be title",
            content="""This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.""",
            user=self.user,
        )

    def test_object_instance(self):
        assert isinstance(self.post, Post)
        assert isinstance(self.not_p_post, Post)
        assert isinstance(Post.objects.get_published()[0], Post)

    def test_return_values(self):
        assert self.post.status == "P"
        assert self.post.status != "p"
        assert self.not_p_post.status == "D"
        assert str(self.post) == "A really nice title"
        assert self.post in Post.objects.get_published()
        assert Post.objects.get_published()[0].title == "A really nice title"
        assert self.not_p_post in Post.objects.get_drafts()
