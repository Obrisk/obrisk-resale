from django.urls import reverse
from django.test import Client

# from elasticsearch_dsl.connections import connections
from test_plus.test import TestCase

from obrisk.classifieds.models import Classified
from obrisk.qa.models import Question
from obrisk.stories.models import Stories
# from obrisk.search.views import all_search

# documents
# from obrisk.users.documents import UsersDocument
# from obrisk.stories.documents import StoriesDocument
# from obrisk.classifieds.document import ClassifiedDocument
# from obrisk.posts.documents import PostsDocument
# from obrisk.qa.documents import QuestionDocument


class SearchViewsTests(TestCase):
    model = Classified
    """
    Includes tests for all the functionality
    associated with Views
    """
    def setUp(self):
        self.user = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
        self.title = "A really nice to-be first title "
        self.details = """This is a really good content, just if somebody
        published it, that would be awesome, but no, nobody wants to publish
        it, because they know this is just a test, and you know than nobody
        wants to publish a test, just a test; everybody always wants the real
        deal."""
        self.classified = Classified.objects.create(
            user=self.user, title="A really nice first title",
            details=self.details, tags="list, lists", status="P")
        self.classified_2 = Classified.objects.create(user=self.other_user,
                                                title="A first bad title",
                                                details="First bad content",
                                                tags="bad", status="P")
        self.question_one = Question.objects.create(
            user=self.user, title="This is the first sample question",
            content="This is a sample question description for the first time",
            tags="test1,test2")
        self.question_two = Question.objects.create(
            user=self.user,
            title="The first shortes title",
            content="""This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it first, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.""",
            has_answer=True, tags="test1,test2"
        )
        self.stories_one = Stories.objects.create(user=self.user,
                                            content="This is the first lazy content.")

    def test_stories_search_results(self):
        response = self.client.get(
            reverse("search:results"), {'query': 'This is'})
        assert response.status_code == 200
        assert self.stories_one in response.context["stories_list"]
        assert self.question_one in response.context["questions_list"]
        assert self.question_two in response.context["questions_list"]
        assert self.classified in response.context["classifieds_list"]

    # def test_questions_suggestions_results(self):
        # response = self.client.get(
            # reverse("search:suggestions"), {'term': 'first'})
            # HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # assert response.json()[0]['value'] == "first_user"
        # assert response.json()[1]['value'] == "A first bad title"
        # assert response.json()[2]['value'] == "A really nice first title"
        # assert response.json()[3]['value'] == "The first shortes title"
        # assert response.json()[4]['value'] == "This is the first sample question"

# class ElasticSearchViewsTests(TestCase):
#    model = Classified
#    """
#    Includes tests for all the functionality
#    associated with Views
#    """
#    def setUp(self):
#        connections.create_connection()
#
#        self.user = self.make_user("sele")
#        self.other_user = self.make_user("emma")
#        self.client = Client()
#        self.other_client = Client()
#        self.client.login(username="sele", password="password")
#        self.other_client.login(username="emma", password="password")
#        self.title = "A really nice to-be first title "
#        self.details = "This is a really good content, just if somebody\
#        published it, that would be awesome, but no, nobody wants to publish\
#        it, because they know this is just a test, and you know than nobody\
#        wants to publish a test, just a test; everybody always wants the real\
#        deal."
#        UsersDocument.init()
#        self.classified = UsersDocument(username=self.user)
#
#
#    def test_all_search(self):
#        response = self.client.get(reverse("search:elastic_results"))
#        assert self.user == self.classified
