from django.test import RequestFactory

from test_plus.test import TestCase
from obrisk.users import models
from obrisk.users.models import User

from ..views import (
    UserRedirectView,
    UserUpdateView
)

#FRIENDSHIP AND FOLLOWERS
import os
#from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.models import Friend, Follow, FriendshipRequest, Block
from friendship.tests import tests


TEST_TEMPLATES = os.path.join(os.path.dirname(__file__), 'templates')

class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()


class TestUserRedirectView(BaseUserTestCase):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = UserRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        view.request = request
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            view.get_redirect_url(),
            '/users/testuser/'
        )


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super().setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = UserUpdateView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request

    def test_get_success_url(self):
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            self.view.get_success_url(),
            '/users/testuser/'
        )

    def test_get_object(self):
        # Expect: self.user, as that is the request's user object
        self.assertEqual(
            self.view.get_object(),
            self.user
        )


#FRIENDSHIP TESTS
class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()

class BaseTestCase(TestCase):
    
    def setUp(self):
        """
        Setup some initial users
        """
        self.user_pw = 'test'
        self.user_bob = self.create_user('bob', 'bob@bob.com', self.user_pw)
        self.user_steve = self.create_user('steve', 'steve@steve.com', self.user_pw)
        self.user_susan = self.create_user('susan', 'susan@susan.com', self.user_pw)
        self.user_amy = self.create_user('amy', 'amy@amy.amy.com', self.user_pw)
        cache.clear()

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def login(self, user, password):
        return login(self, user, password)

    def create_user(self, username, password, email_address):
        user = User.objects.create_user(username, password, email_address)
        return user

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse302(self, response):
        self.assertEqual(response.status_code, 302)

    def assertResponse403(self, response):
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)


class FriendshipViewTests(BaseTestCase):
    def setUp(self):
        self.user_pw = 'test'
        self.user_bob = self.create_user('bob', 'bob@bob.com', self.user_pw)
        self.user_steve = self.create_user('steve', 'steve@steve.com', self.user_pw)
        self.user_susan = self.create_user('susan', 'susan@susan.com', self.user_pw)
        self.user_amy = self.create_user('amy', 'amy@amy.amy.com', self.user_pw)
        super(FriendshipViewTests, self)
        self.friendship_request = Friend.objects.add_friend(self.user_steve, self.user_bob)

    def test_friendship_view_friends(self):
        url = reverse('friendship_view_friends', kwargs={'username': self.user_bob.username})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)
        self.assertTrue('user' in response.context)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_NAME='object', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object' in response.context)

    
    def test_friendship_requests(self):
        url = reverse('friendship_request_list')

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

    def test_friendship_accept(self):
        url = reverse('friendship_accept', kwargs={'friendship_request_id': self.friendship_request.pk})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_requests_detail view
            response = self.client.get(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_requests_detail', kwargs={'friendship_request_id': self.friendship_request.pk})
            self.assertTrue(redirect_url in response['Location'])

    def test_friendship_followers(self):
        url = reverse('friendship_followers', kwargs={'username': 'bob'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_NAME='object', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object' in response.context)

    def test_friendship_following(self):
        url = reverse('friendship_following', kwargs={'username': 'bob'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_NAME='object', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object' in response.context)

    def test_follower_add(self):
        url = reverse('follower_add', kwargs={'followee_username': self.user_amy.username})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

            # on POST accept the friendship request and redirect to the
            # friendship_following view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_following', kwargs={'username': self.user_bob.username})
            self.assertTrue(redirect_url in response['Location'])

            response = self.client.post(url)
            self.assertResponse200(response)
            self.assertTrue('errors' in response.context)
            self.assertEqual(response.context['errors'], ["User 'bob' already follows 'amy'"])

    def test_friendship_blockers(self):
        url = reverse('friendship_blockers', kwargs={'username': 'bob'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_NAME='object', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object' in response.context)

    def test_friendship_blocking(self):
        url = reverse('friendship_blocking', kwargs={'username': 'bob'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_NAME='object', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object' in response.context)

    def test_block_add(self):
        url = reverse('block_add', kwargs={'blocked_username': self.user_amy.username})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

            # on POST accept the friendship request and redirect to the
            # friendship_following view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_blocking', kwargs={'username': self.user_bob.username})
            self.assertTrue(redirect_url in response['Location'])

            response = self.client.post(url)
            self.assertResponse200(response)
            self.assertTrue('errors' in response.context)
            self.assertEqual(response.context['errors'], ["User 'bob' already blocks 'amy'"])

    def test_block_remove(self):
        # create a follow relationship so we can test removing a block
        block = Block.objects.add_block(self.user_bob, self.user_amy)

        url = reverse('block_remove', kwargs={'blocked_username': self.user_amy.username})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_blocking', kwargs={'username': self.user_bob.username})
            self.assertTrue(redirect_url in response['Location'])

