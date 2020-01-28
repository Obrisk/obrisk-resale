import os
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.test import Client, override_settings
from test_plus.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.models import Friend, Follow, FriendshipRequest, Block


TEST_TEMPLATES = os.path.join(os.path.dirname(__file__), "templates")



class ConnectionsViewsTests(TestCase):
    
        
    def setUp(self):
        self.User = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse302(self, response):
        self.assertEqual(response.status_code, 302)

    def assertResponse403(self, response):
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)
    

    def test_friendship_view_friends(self):
        url = reverse(
            "connections:friendship_view_friends"
        )
        # assert user = self.User
        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)
        self.assertTrue("user" in response.context)

        with self.settings(
            FRIENDSHIP_CONTEXT_OBJECT_NAME="object", TEMPLATE_DIRS=(TEST_TEMPLATES,)
        ):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue("object" in response.context)

    def test_add_friends(self):
        first_user = self.User

        second_user = self.other_user

        "users are not friends yet"
        self.assertFalse(Friend.objects.are_friends(first_user, second_user))
        
        "second user havent send any request to 1st user or vice versa"
        self.assertFalse(Friend.objects.can_request_send(first_user, second_user))
        
        Friend.objects.add_friend(first_user, second_user)

        self.assertTrue(Friend.objects.can_request_send(first_user, second_user))

