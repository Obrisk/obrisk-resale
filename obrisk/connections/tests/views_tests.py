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
        self.official_user = self.make_user("official_user")
        self.client = Client()
        self.other_client = Client()
        self.official_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
        self.official_client.login(username="official_user", password="password")
        self.user1 = self.make_user('user1')
        self.user1_client = Client()
        self.user1_client.login(username='user', password="password")

        self.user2 = self.make_user('user2')
        self.user2_client = Client()
        self.user2_client.login(username='user2', password="password")

        self.user3 = self.make_user('user3')
        self.user3_client = Client()
        self.user3_client.login(username='user3', password="password")

        self.user4 = self.make_user('user4')
        self.user4_client = Client()
        self.user4_client.login(username='user4', password="password")
        
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
        
         
    def test_friendship_accept(self):
        users_list = ['user1', 'user2', 'user3', 'user4']
        first_user = self.User
        second_user = self.other_user

        #logged_in_users = [first_user, second_user]
       #for u in users_list:
       #    self.u= self.make_user(u)
       #    usr = 'client_'+u
       #    self.usr= Client()
       #    self.usr.login(username=u, password="password")
    

       
        user1 = self.user1
        user2 = self.user2
        user3 = self.user3
        user4 = self.user4


        logg_in_users = [second_user, user1, user2, user3, user4]
      
     
        self.assertFalse(Friend.objects.are_friends(first_user, user1))
        self.assertFalse(Friend.objects.can_request_send(first_user, user2))
        self.assertFalse(Friend.objects.can_request_send(first_user, user3))
        self.assertFalse(Friend.objects.can_request_send(first_user, user4))
        self.assertFalse(Friend.objects.can_request_send(first_user, second_user))
        reqst1 = Friend.objects.add_friend(first_user, user1)
        reqst2 = Friend.objects.add_friend(first_user, user2)
        reqst3 = Friend.objects.add_friend(first_user, user3)
        reqst4 = Friend.objects.add_friend(first_user, user4)
        reqst5 = Friend.objects.add_friend(first_user, second_user)
        #"checking connection sent& recieved"
        self.assertEqual(len(Friend.objects.requests(first_user)), 0)
        self.assertEqual(len(Friend.objects.sent_requests(first_user)), 5)
        reqst1.accept()
        reqst2.accept()
        reqst3.accept()
        reqst4.accept()
        reqst5.accept()
        #for u in logg_in_users:
        #    self.assertFalse(Friend.objects.are_friends(first_user, u))
        #    self.assertFalse(Friend.objects.can_request_send(first_user, u))
        #    reqst1 = Friend.objects.add_friend(first_user, u)
        #    reqst5.accept()

    
    def test_follower_add(self):
        official_user = self.official_user
        user1 = self.user1
        user2 = self.user2
        user3 = self.user3
        user4 = self.user4
        Follow.objects.add_follower(official_user, user1)
        Follow.objects.add_follower(official_user, user2)
        Follow.objects.add_follower(official_user, user3)
        Follow.objects.add_follower(official_user, user4)
        self.assertEqual(len(Follow.objects.following(official_user)), 4)


