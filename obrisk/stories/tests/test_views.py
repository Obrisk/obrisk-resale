from django.test import Client
from django.urls import reverse

from test_plus.test import TestCase

from obrisk.stories.models import Stories


class StoriesViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
        self.first_stories = Stories.objects.create(
            user=self.user,
            content="This is a short content."
        )
        self.second_stories = Stories.objects.create(
            user=self.user,
            content="This the second content."
        )
        self.third_stories = Stories.objects.create(
            user=self.other_user,
            content="This is an answer to the first stories.",
            reply=True,
            parent=self.first_stories
        )

    def test_stories_list(self):
        response = self.client.get(reverse("stories:list"))
        assert response.status_code == 200
        assert self.first_stories in response.context["stories_list"]
        assert self.second_stories in response.context["stories_list"]
        assert self.third_stories not in response.context["stories_list"]

    def test_delete_stories(self):
        initial_count = Stories.objects.count()
        response = self.client.post(
            reverse("stories:delete_stories", kwargs={"pk": self.second_stories.pk}))
        assert response.status_code == 302
        assert Stories.objects.count() == initial_count - 1

    def test_post_stories(self):
        initial_count = Stories.objects.count()
        response = self.client.post(
            reverse("stories:post_stories"), {"post": "This a third element."},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert Stories.objects.count() == initial_count + 1

    def test_like_stories(self):
        response = self.client.post(
            reverse("stories:like_post"),
            {"stories": self.first_stories.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 405
        assert self.first_stories.count_likers() == 0
        #assert self.user in self.first_stories.get_likers()
        #assert response.json()["likes"] == 1

    def test_thread(self):
        response = self.client.get(
            reverse("stories:get_thread"),
            {"stories": self.first_stories.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert response.json()["uuid"] == str(self.first_stories.pk)
        assert "This is a short content." in response.json()["stories"]
        assert "This is an answer to the first stories." in response.json()["thread"]

    def test_posting_comments(self):
        response = self.client.post(
            reverse("stories:post_comments"),
            {
                "reply": "This a third element.",
                "parent": self.second_stories.pk
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert response.json()["comments"] == 1

    def test_updating_interactions(self):
        first_response = self.client.post(
            reverse("stories:like_post"),
            {"stories": self.first_stories.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        second_response = self.other_client.post(
            reverse("stories:like_post"),
            {"stories": self.first_stories.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        third_response = self.client.post(
            reverse("stories:post_comments"),
            {
                "reply": "This a third element.",
                "parent": self.first_stories.pk
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        fourth_response = self.client.post(
            reverse("stories:update_interactions"),
            {"id_value": self.first_stories.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert first_response.status_code == 405
        assert second_response.status_code ==405
        assert third_response.status_code == 200
        assert fourth_response.status_code == 200
        assert fourth_response.json()["likes"] == 0
        assert fourth_response.json()["comments"] == 2
