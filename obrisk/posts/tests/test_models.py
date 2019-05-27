from test_plus.test import TestCase

from obrisk.posts.models import Post, Jobs, Events


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


#JOBS 

class JobsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Jobs.objects.create(title='Big', details='Bobs birthday', location='tingsong', requirements='student_id', eligibility='students', deadline='2019-05-29', contacts='ibrahim')

    def test_title_label(self):
        jobs = Jobs.objects.get(id=1)
        field_label = jobs._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_details_label(self):
        jobs=Jobs.objects.get(id=1)
        field_label = jobs._meta.get_field('details').verbose_name
        self.assertEquals(field_label, 'details')


    def test_location_label(self):
        jobs=Jobs.objects.get(id=1)
        field_label = jobs._meta.get_field('location').verbose_name
        self.assertEquals(field_label, 'location')

    def test_requirements_label(self):
        jobs=Jobs.objects.get(id=1)
        field_label = jobs._meta.get_field('requirements').verbose_name
        self.assertEquals(field_label, 'requirements')

    def test_contacts_label(self):
        jobs=Jobs.objects.get(id=1)
        field_label = jobs._meta.get_field('contacts').verbose_name
        self.assertEquals(field_label, 'contacts')

    def test_eligibility_label(self):
        jobs=Jobs.objects.get(id=1)
        field_label = jobs._meta.get_field('eligibility').verbose_name
        self.assertEquals(field_label, 'eligibility')

#EVENTS
class EventsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Events.objects.create(title='Bigbon day', address='Bobs room', starting_time='2019-05-25', description='student certificate awarding ceremny', ending_time='2019-05-29', contacts='ibrahim')

    def test_title_label(self):
        events =  Events.objects.get(id=1)
        field_label = events._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_description_label(self):
        events= Events.objects.get(id=1)
        field_label = events._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')


    def test_address_label(self):
        events= Events.objects.get(id=1)
        field_label = events._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_starting_time_label(self):
        events= Events.objects.get(id=1)
        field_label = events._meta.get_field('starting_time').verbose_name
        self.assertEquals(field_label, 'starting time')

    def test_contacts_label(self):
        events= Events.objects.get(id=1)
        field_label = events._meta.get_field('contacts').verbose_name
        self.assertEquals(field_label, 'contacts')

    def test_ending_time_label(self):
        events= Events.objects.get(id=1)
        field_label = events._meta.get_field('ending_time').verbose_name
        self.assertEquals(field_label, 'ending time')
