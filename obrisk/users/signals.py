from django.shortcuts import redirect
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from obrisk.users.tasks import update_profile_picture


@receiver(user_signed_up)
def social_user_connected(user, **kwargs):
    ''' A function which checks the signedin user if has
    a social account anf if the account is linkedin then
    it uploads the user profile picture from linkedin as
    His or her profile picture'''

    if user.socialaccount_set.all() and not user.picture:
        # Checking if the user's provider is linkedin
        update_profile_picture.delay(user_id=user.id)
        return redirect("stories:list")

    else:
        return redirect("stories:list")
