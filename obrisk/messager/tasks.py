import os
import ast
import uuid
from datetime import timedelta

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models.functions import Now
from celery import shared_task
from obrisk.notifications.models import Notification, notification_handler
from obrisk.users.phone_verification import send_sms
from obrisk.messager.models import Conversation, Message
from obrisk.messager.send_wxtemplate import unread_msgs_wxtemplate

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
        cache.set(
            f'msg_{recipient_id}',
            values,
            timeout=SESSION_COOKIE_AGE
        )

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

            ret = send_sms(
                __business_id,
                recipient.phone_number.national_number,
                os.getenv('SMS_SIGNATURE'),
                os.getenv('NOTIF_SMS_TEMPLATE'), params
            )

            ret = ret.decode("utf-8")
            response = ast.literal_eval(ret)

            if response['Code'] == 'OK':
                cache.set(f'notif_sms_{recipient_id}', 1 , 120)


@shared_task
def messages_list_cleanup(conv_key, user_pk, last_receiver_pk):
    unread_msgs = cache.get(f'msg_{user_pk}')
    if unread_msgs is not None:
        values = list(unread_msgs)

        if conv_key in values:
            values = values.remove(conv_key)
            cache.set(
                f'msg_{user_pk}',
                values,
                timeout=SESSION_COOKIE_AGE
            )

    #If update is called on the query, the order 'll be distorted
    if user_pk == last_receiver_pk:
        Conversation.objects.get(
                key=conv_key
            ).messages.all().update(unread=False)


@shared_task
def send_wxtemplate_notif():
    older = Now() - timedelta(seconds=3600)

    notify = {}
    msgs = Message.objects.select_related().filter(
        timestamp__lt=older, unread=True, wx_notified=False
    )

    for msg in msgs:
        wxid = msg.recipient.wechat_openid
        if wxid is None:
            continue
        try:
            if notify[wxid] is None:
                notify[wxid] = [msg]
            else:
                notify[wxid] = notify[wxid].append(msg)
        except KeyError:
            notify[wxid] = [msg]

        msg.wx_notified = True
        msg.save()

    for userid in notify:
        if notify[userid] is None:
            continue

        if notify[userid][-1].message:
            last_msg = notify[userid][-1].message[:60] + '...'
        else:
            last_msg = 'Message contains attachment'

        senders = len(notify[userid])
        if senders > 1:
            sender = f'{notify[userid][0].sender.username} and {senders} Others'
        else:
            sender = f'{notify[userid][0].sender.username}'
        time =  'Few Minutes ago'
        unread_msgs_wxtemplate(userid, last_msg, sender, time)
