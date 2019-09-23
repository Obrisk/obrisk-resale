from django.core.cache import cache
from django.db.models import Subquery, OuterRef
from obrisk.classifieds.models import Classified
from obrisk.messager.models import Conversation, Message

def cached_queries(request):
    popular_tags = cache.get('popular_tags')

    if popular_tags == None:
        popular_tags = Classified.objects.get_counted_tags()
    
    convs = Conversation.objects.get_conversations(request.user).annotate(
                    unread = Subquery (
                        Message.objects.filter(
                            conversation=OuterRef('pk'),
                        ).values('unread')[:1]
                    ),
                    recipient = Subquery (
                    Message.objects.filter(
                        conversation=OuterRef('pk'),
                    ).values('recipient')[:1]
                )
            )

    new_msgs = None

    if convs.exists():
        for con in convs:
            if request.user.id == con.recipient and con.unread:
                new_msgs = True
                break

    return {'popular_tags': popular_tags, 'new_msgs': new_msgs}