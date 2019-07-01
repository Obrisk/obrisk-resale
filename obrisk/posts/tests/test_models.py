from test_plus.test import TestCase

from obrisk.posts.models import Post, Jobs, Events, JOB_CHOICES


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
        assert isinstance(Post.objects.get_active()[0], Post)

    def test_return_values(self):
        assert self.post.status == "P"
        assert self.post.status != "p"
        assert self.not_p_post.status == "D"
        assert str(self.post) == "A really nice title"
        assert self.post in Post.objects.get_active()
        assert Post.objects.get_active()[0].title == "A really nice title"
        #assert self.not_p_post in Post.objects.get_expired()




from django.test import TestCase

class EventsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        Author.objects.create(
            title='loam',
		    posted_at='pipod',
            host='sdeng',
            venue='uouuog',
            details='tjtt',
            start_time='tjtjk',
            end_time='jtj',
            contacts='eijojtr',
            sponsors='erterjlkj',
            )

    def test_title_label(self):
        events = Events.objects.get(id=1)
        field_label = events._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')
    def test_venue_label(self):
        events = Events.objects.get(id=1)
        field_label = events._meta.get_field('venue').verbose_name
        self.assertEquals(field_label, 'venue')
    def test_host_label(self):
        events = Events.objects.get(id=1)
        field_label = events._meta.get_field('host').verbose_name
        self.assertEquals(field_label, 'host')



    # def test_date_of_death_label(self):
    #     author=Author.objects.get(id=1)
    #     field_label = author._meta.get_field('date_of_death').verbose_name
    #     self.assertEquals(field_label, 'died')

    def test_title_max_length(self):
        events = Events.objects.get(id=1)
        max_length = events._meta.get_field('title').max_length
        self.assertEquals(max_length, 80)
    def test_host_max_length(self):
        events = Events.objects.get(id=1)
        max_length = events._meta.get_field('host').max_length
        self.assertEquals(max_length, 80)
    def test_venue_max_length(self):
        events = Events.objects.get(id=1)
        max_length = events._meta.get_field('venue').max_length
        self.assertEquals(max_length, 80)
