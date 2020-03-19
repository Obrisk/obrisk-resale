from django.core.cache import cache
from django.db.models import Subquery, OuterRef
from obrisk.classifieds.models import Classified
from obrisk.messager.models import Conversation, Message
from django.conf import settings
import environ


def cached_queries(request):
    new_msgs = None

    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

    #if request.user.is_authenticated:
        #Will implement these queries as background tasks.
        #convs = Conversation.objects.get_conversations(request.user).annotate(
                        #unread = Subquery (
                            #Message.objects.filter(
                                #conversation=OuterRef('pk'),
                            #).values('unread')[:1]
                        #),
                        #recipient = Subquery (
                        #Message.objects.filter(
                            #conversation=OuterRef('pk'),
                        #).values('recipient')[:1]
                    #)
                #)

        #if convs.exists():
            #for con in convs:
                #if request.user.id == con.recipient and con.unread:
                    #new_msgs = True
                    #break
    user = User.objects.get(username=request.user)
    msg_notifications = cache.get(f'msg_{user.pk}')
    oss = 'https://obrisk.oss-cn-hangzhou.aliyuncs.com'
    return { 'new_msgs': new_msgs, 'vapid_key':vapid_key, 'oss':oss, 'msg_notifications':msg_notifications}
