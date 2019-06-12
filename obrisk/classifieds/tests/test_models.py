from test_plus.test import TestCase

from obrisk.classifieds.models import Classified


class ClassifiedsModelsTest(TestCase):
    def setUp(self):
        self.User = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
        self.classified = Classified.objects.create(
            title="A really nice title",
            details="This is a really good details",
            status="A",
            user=self.User,
        )
        self.not_p_classified = Classified.objects.create(
            title="A really nice to-be title",
            details="""This is a really good details, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.""",
            user=self.User,
        )

    def test_object_instance(self):
        assert isinstance(self.classified, Classified)
        assert isinstance(self.not_p_classified, Classified)
        assert isinstance(Classified.objects.get_active()[0], Classified)

    def test_return_values(self):
        assert self.classified.status == "A"
        assert self.classified.status != "p"
        assert self.not_p_classified.status == "A"
        assert str(self.classified) == "A really nice title"
        assert self.classified in Classified.objects.get_active()
        assert Classified.objects.get_active()[0].title == "A really nice to-be title"
        assert self.not_p_classified in Classified.objects.get_active()
