import os
import uuid
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from celery import shared_task
from obrisk.notifications.models import Notification, notification_handler
from obrisk.users.phone_verification import send_sms

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User


SESSION_COOKIE_AGE = getattr(
        settings, 'SESSION_COOKIE_AGE', DEFAULT_TIMEOUT
    )

@shared_task
def send_messages_notifications(sender_id, recipient_id, key):
    recp_new_msgs = cache.get(f'msg_{recipient_id}')

    if recp_new_msgs is None:
        cache.set(f'msg_{recipient_id}', [key] , timeout=SESSION_COOKIE_AGE)
    else:
        values = list(recp_new_msgs).append(key)
        cache.set(f'msg_{recipient_id}', values, timeout=SESSION_COOKIE_AGE)

    sender = user_model.objects.get(id=sender_id)
    recipient = user_model.objects.get(id=recipient_id)

    notification_handler(actor=sender,
            recipient=recipient,
            verb=Notification.NEW_MESSAGE,
            is_msg=True, key='new_message')

    msgs_notif = cache.get(f'notif_sms_{recipient_id}')

    if (msgs_notif is None and recipient.phone_number != '' and
            recipient.phone_number.national_number != 13300000000):

        if getattr(settings, 'PHONE_SIGNUP_DEBUG', False):
            print(f'Hi {recipient.username}, you have new msgs')
        else:
            params = " {\"recip\":\""+ recipient.username + "\"} "
            __business_id = uuid.uuid1()

            send_sms(
                __business_id,
                recipient.phone_number.national_number,
                os.getenv('SMS_SIGNATURE'),
                os.getenv('NOTIF_SMS_TEMPLATE'), params
            )

            cache.set(f'notif_sms_{recipient_id}', 1 , 600)
