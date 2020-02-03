import os
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.test import Client, override_settings
from test_plus.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.models import Friend, Follow, FriendshipRequest, Block
from django.contrib.auth import get_user_model
User = get_user_model()

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
        first_user = self.User
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

        friends = Friend.objects.friends(first_user)

        # friends_pk = friends.values_list('id', flat=True)
        friends_pk = [u.id for u in friends]
        friends_pk.append(first_user.id)

        # Try to Get the recommendation list from cache
        recommended_connects = cache.get(f"recommended_connects_{first_user.id}")

        if recommended_connects == None:
            recommended_connects = (
               User.objects.filter(city=first_user.city)
                .exclude(thumbnail=None)
                .exclude(pk__in=friends_pk)[:40]
            )

            RECOMMENDATION_TIMEOUT = getattr(
                settings, "CONNECTS_RECOMMENDATION_TIMEOUT", DEFAULT_TIMEOUT
            )
            cache.set(
                f"recommended_connects_{first_user.id}",
                recommended_connects,
                timeout=RECOMMENDATION_TIMEOUT,
            )
            url = reverse(
            "connections:friendship_view_friends"
        )

            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue("object" in response.context)
 


    def test_add_friends(self):
        first_user = self.User

        second_user = self.other_user
        url = reverse(
            "connections:friendship_add_friend", kwargs={"to_username": second_user}
        )
        # assert user = self.User
        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        #"users are not friends yet"
        self.assertFalse(Friend.objects.are_friends(first_user, second_user))
       
        #"second user havent send any request to 1st user or vice versa"
        self.assertFalse(Friend.objects.can_request_send(first_user, second_user))
       
        Friend.objects.add_friend(first_user, second_user)
        self.assertEqual(
            FriendshipRequest.objects.filter(from_user=self.User).count(), 1
        )
        self.assertTrue(Friend.objects.can_request_send(first_user, second_user))

        #"checking connection sent& recieved"
        first_user = self.User
        second_user = self.other_user
        self.assertEqual(len(Friend.objects.requests(first_user)), 0)
        self.assertEqual(len(Friend.objects.requests(second_user)), 1)
        self.assertEqual(len(Friend.objects.sent_requests(first_user)), 1)
        self.assertEqual(len(Friend.objects.sent_requests(second_user)), 0)
        
         
       
