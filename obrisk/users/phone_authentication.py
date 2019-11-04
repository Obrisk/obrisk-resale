from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneAuthBackend(object):
    """
    Authenticate using a phone number.
    """
    def authenticate(self, request, username=None, password=None):
        #This is a forgiving code, allow users to login with country code.
        phone = str(username)
        if phone.isalpha() and phone.startswith("+86") == False:
            return None
        if len(phone) == 11 and phone[0] != '1':
            return None
        else:
            try:
                #This code only works for Chinese phone numbers.
                if phone.startswith("+86") == False:
                    phone = "+86" + phone
                try:
                    user = User.objects.get(phone_number=phone)
                except:
                    #This is not a right return value on this failure. To improve more in the near future.
                    return None
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