import tempfile

from PIL import Image

from django.test import Client, override_settings
from django.urls import reverse

from test_plus.test import TestCase

from obrisk.classifieds.models import Classified


def get_temp_img():
    size = (200, 200)
    color = (255, 0, 0, 0)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        image = Image.new("RGB", size, color)
        image.save(f, "PNG")

    return open(f.name, mode="rb")


class ClassifiedsViewsTest(TestCase):
    def setUp(self):
        self.User = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
        self.classified = Classified.objects.create(
            title="A really nice title",
            details="This is a really good detail",
            status="P",
            user=self.User,
        )
        self.not_p_classified = Classified.objects.create(
            title="A really nice title",
            details="""This is a really good detail, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.""",
            user=self.User,
        )
        self.test_image = get_temp_img()

    def tearDown(self):
        self.test_image.close()

    def test_index_classifieds(self):
        response = self.client.get(reverse("classifieds:list"))
        self.assertEqual(response.status_code, 200)

    def test_error_404(self):
        response_no_art = self.client.get(reverse(
            "classifieds:classified", kwargs={"slug": "no-slug"}))
        self.assertEqual(response_no_art.status_code, 404)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_classified(self):
        response = self.client.post(reverse("classifieds:write_new"),
                                    {"title": "A not that really nice title",
                                     "details": "Whatever works for you",
                                     "tags": "list, lists",
                                     "status": "P",
                                     "image": self.test_image})
        assert response.status_code == 200

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_single_classified(self):
        current_count = Classified.objects.count()
        response = self.client.post(reverse("classifieds:write_new"),
                                    {"title": "A not that really nice title",
                                     "details": "Whatever works for you",
                                     "tags": "list, lists",
                                     "status": "P",
                                     "image": self.test_image})
        # response_art = self.client.get(
        #     reverse("classifieds:classified",
        #     kwargs={"slug": "a-not-that-really-nice-title"}))
        # assert response_art.status_code == 200
        assert response.status_code == 200
        assert Classified.objects.count() == current_count

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_draft_classified(self):
        response = self.client.post(reverse("classifieds:write_new"),
                                    {"title": "A not that really nice title",
                                     "details": "Whatever works for you",
                                     "tags": "list, lists",
                                     "status": "D",
                                     "image": self.test_image})
        resp = self.client.get(reverse("classifieds:drafts"))
        assert resp.status_code == 200
        assert response.status_code == 200
        assert resp.context["classifieds"][0].slug == "first-user-a-not-that-really-nice-title"
