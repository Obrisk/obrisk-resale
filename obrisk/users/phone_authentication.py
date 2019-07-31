from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneAuthBackend(object):
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            #This code only works for Chinese phone numbers.
            if str(username).startswith("+86") == False:
                username = "+86" + username
            user = User.objects.get(phone_number=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None