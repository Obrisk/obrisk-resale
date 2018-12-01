from test_plus.test import TestCase

from obrisk.stories.models import Stories


class StoriesModelsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
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

    def test_reply_this(self):
        initial_count = Stories.objects.count()
        self.first_stories.reply_this(self.other_user, "A second answer.")
        assert Stories.objects.count() == initial_count + 1
        assert self.first_stories.count_thread() == 2
        assert self.third_stories in self.first_stories.get_thread()

    def test_switch_like(self):
        self.first_stories.switch_like(self.user)
        assert self.first_stories.count_likers() == 1
        assert self.user in self.first_stories.get_likers()
