from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class PhoneAuthBackend(ModelBackend):
    """
    Authenticate using a phone number.
    """
    def __init__(self, *args, **kwargs):
        self.user_model = get_user_model()

    
    def get_phone_number_data(self, phone):
        """
        Method used for filtering query.
        """
        data = {
            'phone_number': phone
        }
        return data

    def authenticate(self, request, username=None, password=None):
        #This is a forgiving code, allow users to login with country code.
        phone = str(username)
        print(phone.isalpha())
        if phone.startswith("+86"):
            phone = phone.strip('+86')
        
        
        if phone.isdigit() and len(phone) == 11 and phone[0] == '1':
            #This code only works for Chinese phone numbers.
            phone = "+86" + phone
            
            user = self.user_model.objects.filter(
                    **self.get_phone_number_data(phone)
                ).first()
            
            if not user:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                self.user_model().set_password(password)
            else:
                if user.check_password(password):
                    return user