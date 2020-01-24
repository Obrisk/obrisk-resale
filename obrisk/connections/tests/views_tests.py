import os
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.models import Friend, Follow, FriendshipRequest, Block


TEST_TEMPLATES = os.path.join(os.path.dirname(__file__), "templates")


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success, "login with username=%r, password=%r failed" % (user, password)
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
        self.user_pw = "test"
        self.user_bob = self.create_user("bob", "bob@bob.com", self.user_pw)
        self.user_steve = self.create_user("steve", "steve@steve.com", self.user_pw)
        self.user_susan = self.create_user("susan", "susan@susan.com", self.user_pw)
        self.user_amy = self.create_user("amy", "amy@amy.amy.com", self.user_pw)
        cache.clear()

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def login(self, user, password):
        return login(self, user, password)

    def create_user(self, username, email_address, password):
        user = User.objects.create_user(username, email_address, password)
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
        super(FriendshipViewTests, self).setUp()
        self.friendship_request = Friend.objects.add_friend(
            self.user_steve, self.user_bob
        )

    # def test_friendship_view_users(self):
    #     url = reverse("friendship_view_users")

    #     # test that the view requires authentication to access it
    #     response = self.client.get(url)
    #     self.assertResponse200(response)

    #     with self.settings(
    #         FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME="object_list",
    #         TEMPLATE_DIRS=(TEST_TEMPLATES,),
    #     ):
    #         response = self.client.get(url)
    #         self.assertResponse200(response)
    #         self.assertTrue("object_list" in response.context)

    def test_friendship_view_friends(self):
        url = reverse(
            "connections:friendship_view_friends"
        )

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

    def test_friendship_add_friend(self):
        url = reverse(
            "connections:friendship_add_friend",
        )

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_add_friend view
            response = self.client.get(url)
            self.assertResponse200(response)

            # on POST accept the friendship request and redirect to the
            # friendship_request_list view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse("connections:friendship_request_list")
            self.assertTrue(redirect_url in response["Location"])

    def test_friendship_add_friend_dupe(self):
        url = reverse(
            "connections:friendship_add_friend",
        )

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_add_friend view

            # on POST accept the friendship request and redirect to the
            # friendship_request_list view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse("connections:friendship_request_list")
            self.assertTrue(redirect_url in response["Location"])

            response = self.client.post(url)
            self.assertResponse200(response)
            self.assertTrue("errors" in response.context)
            self.assertEqual(
                response.context["errors"], ["Friendship already requested"]
            )

    def test_friendship_requests(self):
        url = reverse("connections:friendship_request_list")

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

    def test_friendship_requests_rejected(self):
        url = reverse("connections:friendship_requests_rejected")

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

    def test_friendship_accept(self):
        url = reverse(
            "connections:friendship_accept",
            kwargs={"friendship_request_id": self.friendship_request.pk},
        )

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_requests_detail view
            response = self.client.get(url)
            self.assertResponse302(response)
            redirect_url = reverse(
                "connections:friendship_requests_detail",
                kwargs={"friendship_request_id": self.friendship_request.pk},
            )
            self.assertTrue(redirect_url in response["Location"])

            # on POST accept the friendship request and redirect to the
            # friendship_view_friends view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse(
                "connections:friendship_view_friends", kwargs={"username": self.user_bob.username}
            )
            self.assertTrue(redirect_url in response["Location"])

        with self.login(self.user_steve.username, self.user_pw):
            # on POST try to accept the friendship request
            # but I am logged in as Steve, so I cannot accept
            # a request sent to Bob
            response = self.client.post(url)
            self.assertResponse404(response)

    def test_friendship_reject(self):
        url = reverse(
            "connections:friendship_reject",
            kwargs={"friendship_request_id": self.friendship_request.pk},
        )

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_requests_detail view
            response = self.client.get(url)
            self.assertResponse200(response)
            redirect_url = reverse(
                "connections:friendship_requests_detail",
                kwargs={"friendship_request_id": self.friendship_request.pk},
            )
            self.assertTrue(redirect_url in response["Location"])

            # on POST reject the friendship request and redirect to the
            # friendship_requests view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse("connections:friendship_request_list")
            self.assertTrue(redirect_url in response["Location"])

        with self.login(self.user_steve.username, self.user_pw):
            # on POST try to reject the friendship request
            # but I am logged in as Steve, so I cannot reject
            # a request sent to Bob
            response = self.client.post(url)
            self.assertResponse404(response)

    def test_friendship_cancel(self):
        url = reverse(
            "connections:friendship_cancel",
            kwargs={"friendship_request_id": self.friendship_request.pk},
        )

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_requests_detail view
            response = self.client.get(url)
            self.assertResponse302(response)
            redirect_url = reverse(
                "connections:friendship_requests_detail",
                kwargs={"friendship_request_id": self.friendship_request.pk},
            )
            self.assertTrue(redirect_url in response["Location"])

            # on POST try to cancel the friendship request
            # but I am logged in as Bob, so I cannot cancel
            # a request made by Steve
            response = self.client.post(url)
            self.assertResponse404(response)

        with self.login(self.user_steve.username, self.user_pw):
            # on POST cancel the friendship request and redirect to the
            # friendship_requests view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse("connections:friendship_request_list")
            self.assertTrue(redirect_url in response["Location"])

    def test_friendship_requests_detail(self):
        url = reverse(
            "connections:friendship_requests_detail",
            kwargs={"friendship_request_id": self.friendship_request.pk},
        )

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

    def test_friendship_followers(self):
        user = re
        url = reverse("connections:friendship_followers")

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(
            FRIENDSHIP_CONTEXT_OBJECT_NAME="object", TEMPLATE_DIRS=(TEST_TEMPLATES,)
        ):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue("object" in response.context)

    def test_friendship_following(self):
        url = reverse("connections:friendship_following")

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(
            FRIENDSHIP_CONTEXT_OBJECT_NAME="object", TEMPLATE_DIRS=(TEST_TEMPLATES,)
        ):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue("object" in response.context)

    def test_follower_add(self):
        url = reverse(
            "connections:follower_add", kwargs={"followee_username": self.user_amy.username}
        )

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
            redirect_url = reverse(
                "connections:friendship_following", kwargs={"username": self.user_bob.username}
            )
            self.assertTrue(redirect_url in response["Location"])

            response = self.client.post(url)
            self.assertResponse200(response)
            self.assertTrue("errors" in response.context)
            self.assertEqual(
                response.context["errors"], ["User 'bob' already follows 'amy'"]
            )

    def test_follower_remove(self):
        # create a follow relationship so we can test removing a follower
        follow = Follow.objects.add_follower(self.user_bob, self.user_amy)

        url = reverse(
            "connections:follower_remove", kwargs={"followee_username": self.user_amy.username}
        )

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse(
                "connections:friendship_following", kwargs={"username": self.user_bob.username}
            )
            self.assertTrue(redirect_url in response["Location"])

    def test_friendship_blockers(self):
        url = reverse("connections:friendship_blockers", kwargs={"username": "bob"})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(
            FRIENDSHIP_CONTEXT_OBJECT_NAME="object", TEMPLATE_DIRS=(TEST_TEMPLATES,)
        ):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue("object" in response.context)

    def test_friendship_blocking(self):
        url = reverse("connections:friendship_blocking", kwargs={"username": "bob"})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(
            FRIENDSHIP_CONTEXT_OBJECT_NAME="object", TEMPLATE_DIRS=(TEST_TEMPLATES,)
        ):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue("object" in response.context)

    def test_block_add(self):
        url = reverse("connections:block_add", kwargs={"blocked_username": self.user_amy.username})

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
            redirect_url = reverse(
                "connections:friendship_blocking", kwargs={"username": self.user_bob.username}
            )
            self.assertTrue(redirect_url in response["Location"])

            response = self.client.post(url)
            self.assertResponse200(response)
            self.assertTrue("errors" in response.context)
            self.assertEqual(
                response.context["errors"], ["User 'bob' already blocks 'amy'"]
            )

    def test_block_remove(self):
        # create a follow relationship so we can test removing a block
        block = Block.objects.add_block(self.user_bob, self.user_amy)

        url = reverse(
            "connections:block_remove", kwargs={"blocked_username": self.user_amy.username}
        )

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse(
                "connections:friendship_blocking", kwargs={"username": self.user_bob.username}
            )
            self.assertTrue(redirect_url in response["Location"])

