import tempfile

from PIL import Image

from django.test import Client, override_settings
from django.urls import reverse

from test_plus.test import TestCase

from obrisk.posts.models import Post, Jobs, JOB_CHOICES, Events


def get_temp_img():
    size = (200, 200)
    color = (255, 0, 0, 0)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        image = Image.new("RGB", size, color)
        image.save(f, "PNG")

    return open(f.name, mode="rb")


class PostsViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
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
        self.test_image = get_temp_img()

    def tearDown(self):
        self.test_image.close()

    def test_index_posts(self):
        response = self.client.get(reverse("posts:list"))
        self.assertEqual(response.status_code, 200)

    def test_error_404(self):
        response_no_art = self.client.get(reverse(
            "posts:post", kwargs={"slug": "no-slug"}))
        self.assertEqual(response_no_art.status_code, 404)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_Post(self):
        response = self.client.post(reverse("posts:write_new"),
                                    {"title": "A not that really nice title",
                                     "content": "Whatever works for you",
                                     "tags": "list, lists",
                                     "status": "P",
                                     "image": self.test_image})
        assert response.status_code == 200

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_single_Post(self):
        current_count = Post.objects.count()
        response = self.client.post(reverse("posts:write_new"),
                                    {"title": "A not that really nice title",
                                     "content": "Whatever works for you",
                                     "tags": "list, lists",
                                     "status": "P",
                                     "image": self.test_image})
        # response_art = self.client.get(
        #     reverse("Posts:Post",
        #     kwargs={"slug": "a-not-that-really-nice-title"}))
        # assert response_art.status_code == 200
        assert response.status_code == 200
        assert Post.objects.count() == current_count

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_draft_Post(self):
        response = self.client.post(reverse("posts:write_new"),
                                    {"title": "A not that really nice title",
                                     "content": "Whatever works for you",
                                     "tags": "list, lists",
                                     "status": "D",
                                     "image": self.test_image})
        resp = self.client.get(reverse("posts:drafts"))
        assert resp.status_code == 200
        assert response.status_code == 200
        #ssert resp.context["posts"][0].slug == "first-user-a-really-to-be-nice-title"
