from allauth.socialaccount.models import SocialAccount
# from obrisk.users.serializers import UserSerializer 

from django.test import RequestFactory
from test_plus.test import TestCase

from ..views import (
    UserRedirectView,
    UserUpdateView,
 #    complete_authentication,
)


# social_user = User.objects.create(username='test_user')
# SocialAccount.objects.create(user=social_user, id=12, uid='QWCERTGD', ken='fajkhfpualskrjr3n', provider='linkedin_oauth2', user_id=1)

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



# class SocialUserTests(TestCase):
    
#     def setUp(self):
#         self.User = self.create(username='jacob', email='jacob@…', password='top_secret', phone_number= None)
#         self.client = Client()
#         self.client.login(username="first_user", password=None)
# 
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()
#     def assertResponse200(self, response):
#         self.assertEqual(response.status_code, 200)
# 
#     def assertResponse302(self, response):
#        self.assertEqual(response.status_code, 302)

#     def assertResponse403(self, response):
#         self.assertEqual(response.status_code, 403)

#     def assertResponse404(self, response):
#         self.assertEqual(response.status_code, 404)
  

#     def test_complete_authorization(self):
        # Create an instance of a GET request.

#         if not user.phone_number and u.socialaccount_set.all():
#             user_input = {'phone_number' : '+8613243556510', 'password':'@Mi123123 '} 
#             serializer = UserSerializer(user, data=user_input) 
#             assertTrue(serializer.is_valid, True)
#             serializer.save()

#             self.assertTrue(user.phone_number is not None) 
#             self.assertTrue(json.validated_data)
    

