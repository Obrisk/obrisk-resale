from obrisk.users.tasks import update_profile_picture
from django.shortcuts import redirect
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def social_user_connected(user, **kwargs):
    """
    when triggerd, it initiates update profile picture
    backgroundnd task and redirects to the homepage
    """
    if user.socialaccount_set.all() and not user.picture:

        update_profile_picture.delay(user, 'linkedin')

        return redirect("stories:list")
    else:
        return redirect("stories:list")
