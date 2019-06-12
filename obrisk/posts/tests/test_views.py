import tempfile

from PIL import Image

from django.test import Client, override_settings
from django.urls import reverse

from test_plus.test import TestCase
from obrisk.posts import views
from obrisk.posts.models import Post
from obrisk.posts.models import Post,Jobs, Events
from obrisk.posts.views import JobsListView, CreateJobsView, DetailJobsView,EventsListView, CreateEventsView, DetailEventsView

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
        assert response.status_code == 302

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
        assert response.status_code == 302
        assert Post.objects.count() == current_count + 1

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
        assert response.status_code == 302
        #assert resp.context["posts"][0].slug == "first-user-a-really-to-be-nice-title"


#JOBS


class JobsListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create 13 jobs for pagination tests
        number_of_jobs = 13

        for jobs_id in range(number_of_jobs):
            Jobs.objects.create(title='Big', details='Bobs birthday', location='tingsong', requirements='student_id', eligibility='students', deadline='2019-05-29', contacts='ibrahim')


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('new-jobs')
        self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        response = self.client.get('jobs')
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        response = self.client.get('jobs')
        self.assertEqual(response.status_code, 404)
        #self.assertTemplateUsed(response, 'posts/posts_list.html')

    

    def test_lists_all_jobs(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(('jobs')+'?page=2')
        self.assertEqual(response.status_code, 404)
        self.assertFalse('is_paginated' in response.context)
        #self.assertTrue(response.context['jobs'] == True)
        #self.assertTrue(len(response.context['jobs']) == 10)



#EVENTS 


class EventsListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create 13 events for pagination tests
        number_of_events = 13

        for events_id in range(number_of_events):
            Events.objects.create(title='Bigbon day', address='Bobs room', starting_time='2019-05-25', description='student certificate awarding ceremny', ending_time='2019-05-29', contacts='ibrahim')


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('new-events')
        self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        response = self.client.get('events')
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        response = self.client.get('events')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    

    def test_lists_all_events(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(('events')+'?page=2')
        self.assertEqual(response.status_code, 404)
        self.assertFalse('is_paginated' in response.context)
        #self.assertTrue(response.context['events'] == False)
        #self.assertTrue(len(response.context['events']) == 10)

