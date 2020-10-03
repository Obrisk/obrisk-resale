#Please ignore pylint hint on Classified.DoesNotExist
#This code is valid
import time
import base64
import datetime
import oss2
import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.cache import cache
from django.views.generic import ListView
from django.db.models import OuterRef, Subquery

from slugify import slugify
from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.messager.models import Message, Conversation
from obrisk.utils.helpers import ajax_required
from obrisk.utils.images_upload import bucket, bucket_name
from obrisk.notifications.models import Notification, notification_handler

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User


class ContactsListView(LoginRequiredMixin, ListView):
    """This CBV is used to filter the list of contacts in the user"""
    """and allow the user to select the active one before chatting"""
    model = Message
    paginate_by = 50
    template_name = "messager/contact_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        #Instead of running this query, be storing the last image on every conversation.
        context['convs'] = Conversation.objects.get_conversations(
                        self.request.user
                    ).select_related('first_user','second_user').annotate(
                        time = Subquery (
                            Message.objects.filter(
                                conversation=OuterRef('pk'),
                            ).values_list('timestamp', flat=True).order_by('-timestamp')[:1]
                        ),
                        last_msg = Subquery (
                            Message.objects.filter(
                                conversation=OuterRef('pk'),
                            ).values_list('message', flat=True).order_by('-timestamp')[:1]
                        ),
                        img = Subquery (
                            Message.objects.filter(
                                conversation=OuterRef('pk'),
                            ).values_list('image', flat=True).order_by('-timestamp')[:1]
                        ),
                        attachment = Subquery (
                            Message.objects.filter(
                                conversation=OuterRef('pk'),
                            ).values_list('attachment', flat=True).order_by('-timestamp')[:1]
                        ),
                        unread = Subquery (
                            Message.objects.filter(
                                conversation=OuterRef('pk'),
                            ).values_list('unread', flat=True).order_by('-timestamp')[:1]
                        ),
                        recipient = Subquery (
                            Message.objects.filter(
                                conversation=OuterRef('pk'),
                            ).values_list('recipient', flat=True).order_by('-timestamp')[:1]
                        )
                ).order_by('-time')

        context['super_users'] = get_user_model().objects.filter(is_superuser=True)
        context['base_active'] = 'chat'

        #This is for active user in the messages.js, I was trying to quickly make push notifications work
        #now there is probably no need.
        if context['convs']:
            if context['convs'][0].first_user == self.request.user:
                context['active'] = context['convs'][0].second_user.username
            else:
                context['active'] = context['convs'][0].first_user.username
        return context


@ensure_csrf_cookie
@login_required
@require_http_methods(["GET"])
def messagesView(request, username):
    """CBV to render the inbox, showing a specific conversation with a given
    user, who requires to be active too."""
    if request.method == 'GET':
        try:
            active_user = get_user_model().objects.get(
                        username=username)

        except get_user_model().DoesNotExist:
            return JsonResponse({
                'status': '404',
                'message': 'This user does not exist'
            })

        else:
            key = "{}.{}".format(*sorted([request.user.pk, active_user.pk]))

            conv, is_created = Conversation.objects.get_or_create(key=key)
            if is_created:
                conv.first_user = request.user
                conv.second_user = active_user
                conv.save()

            msgs_all = conv.messages.all().select_related(
                    'sender',
                    'recipient',
                    'classified'
                ).values('message',
                        'timestamp',
                        'classified_thumbnail',
                        'img_preview',
                        'image',
                        'unread').annotate(
                    sender_username = Subquery (
                        user_model.objects.filter(
                            sent_messages=OuterRef('pk'),
                        ).values_list('username', flat=True)[:1]),
                    sender_thumbnail = Subquery (
                        user_model.objects.filter(
                            sent_messages=OuterRef('pk'),
                        ).values_list('thumbnail', flat=True)[:1]),
                    recipient_username = Subquery (
                        user_model.objects.filter(
                            received_messages=OuterRef('pk'),
                        ).values_list('username', flat=True)[:1]),
                    recipient_thumbnail = Subquery (
                        user_model.objects.filter(
                            received_messages=OuterRef('pk'),
                        ).values_list('thumbnail', flat=True)[:1]),
                    classified_title = Subquery (
                        Classified.objects.filter(
                            message=OuterRef('pk'),
                        ).values_list('title', flat=True)[:1]),
                    classified_price = Subquery (
                        Classified.objects.filter(
                            message=OuterRef('pk'),
                        ).values_list('price', flat=True)[:1]),
                    classified_slug = Subquery (
                        Classified.objects.filter(
                            message=OuterRef('pk'),
                        ).values_list('slug', flat=True)[:1]),
                    )

            msgs_data = list(msgs_all)

            #If update is called on the query, the order 'll be distorted
            msgs_all.update(unread=False)

            unread_msgs = cache.get(f'msg_{request.user.pk}')
            if unread_msgs is not None:
                values = list(unread_msgs)

                if key in values:
                    values = values.remove(key)
                    cache.set(f'msg_{request.user.pk}', values, None)

            #Slicing is at end to allow the update query to run
            return JsonResponse({
                'msgs': msgs_data[:50],
                'active_username': active_user.username,
                'active_thumbnail': active_user.thumbnail
            })

    else:
        return JsonResponse ({
            'status': '403',
            'message': 'Invalid request'
        })


@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """AJAX view to recieve just the minimum information,
    and create the new message and return the new data
    to be attached to the conversation stream."""
    sender = request.user
    recipient_username = request.POST.get('to')
    try:
        recipient = get_user_model().objects.get(
                    username=recipient_username
                )
    except get_user_model().DoesNotExist:
        return HttpResponseNotFound(
                "This account doesn't exist or it is freezed!")

    #Django-channels doesn't accept group names that are chinese
    #This is a trivial workaround to avoid an error to happen
    #in case the name of user is in chinese characters

    recipient.username = slugify(recipient_username)
    sender.username = slugify(request.user.username)

    message = request.POST.get('message')
    image = request.POST.get('image')
    attachment = request.POST.get('attachment')
    img_preview=None

    if not message and not image and not attachment:
        return HttpResponse()

    if image:
        if image.startswith(
            f'media/images/messages/{sender.username}/{recipient.username}' #noqa
          ) == False:
            image = None

        else:
            d = str(datetime.datetime.now())
            img_preview = "media/images/messages/" + slugify(
                    str(request.user.username)) + "/" + slugify(
                            str(recipient_username)
                        ) + "/preview/" + "prv-" + d + ".jpeg"
            style1 = 'image/resize,m_fill,h_250,w_250'

            try:
                process1 = "{0}|sys/saveas,o_{1},b_{2}".format(style1,
                                                            oss2.compat.to_string(
                                                                base64.urlsafe_b64encode(
                                                                oss2.compat.to_bytes(img_preview))),
                                                            oss2.compat.to_string(
                                                                base64.urlsafe_b64encode(
                                                                    oss2.compat.to_bytes(bucket_name))))
                bucket.process_object(image, process1)
            except:
                image = None
                img_preview = None

    if message and len(message.strip()) == 0:
        return HttpResponse()

    if sender != recipient:
        msg = Message.send_message(sender, recipient, message,
                            image=image, img_preview=img_preview,
                            attachment=attachment)
        notification_handler(actor=sender,
                recipient=recipient,
                verb=Notification.NEW_MESSAGE,
                is_msg=True, key='new_message')

        key = "{}.{}".format(*sorted([sender.pk, recipient.pk]))

        recp_new_msgs = cache.get(f'msg_{recipient.pk}')
        if recp_new_msgs is None:
            cache.set(f'msg_{recipient.pk}', [key] , None)
        else:
            values = list(recp_new_msgs).append(key)
            cache.set(f'msg_{recipient.pk}', values, None)

        # creating a key for the chatting users and updating a value for the key
        # value = "{}.{}".format(*sorted([sender.pk, recipient.pk]))
        # cache.set(f'joint_chat_{sender.pk}', value, timeout=SESSION_COOKIE_AGE)

        # # keys from caches
        # sender_key = cache.get(f'joint_chat_{sender.pk}')
        # recipient_key = cache.get(f'joint_chat_{recipient.pk}')
        # print('sender key:', sender_key, "and recipient key", recipient_key )

        # if recipient_key is None and recipient_key !=sender_key:
        #     #notification
        #     notification_handler(actor=sender, recipient=recipient,
              #verb=Notification.NEW_MESSAGE, is_msg=True, key='message')

        return render(
                request, 'messager/single_message.html',
                {'message': msg}
            )

    return HttpResponse()


@login_required
@ajax_required
@require_http_methods(["GET"])
def receive_message(request):
    """AJAX view to return a rendered single message on the
    receiver side providing realtime connections."""
    try:
        message_id = request.GET.get('message_id')
        message = Message.objects.get(pk=message_id)
    except:
        time.sleep(2)
        message_id = request.GET.get('message_id')
        message = Message.objects.get(pk=message_id)
    return render(request,
                  'messager/single_message.html', {'message': message})


@login_required
@require_http_methods(["GET"])
def classified_chat(request, to, classified):
    """ Create a Conversation object btn 2 users with
    classified post as the initial message """
    try:
        to_user = get_user_model().objects.get(username=to)
        from_user = request.user
        classified = Classified.objects.get(id=classified)

        if classified.user != to_user:
            return redirect('messager:contacts_list')

    except get_user_model().DoesNotExist:
        messages.error(request, f"Sorry, The account {to} is unavailable!")
        return redirect('messager:contacts_list')

    except Classified.DoesNotExist:
        #This error message assumes that the classifieds items
        #are never deleted completely.
        messages.error(
                request,
                f"Invalid request or the classified is unavailable!"
            )
        return redirect('messager:contacts_list')

    else:
        classified_thumbnail = ClassifiedImages.objects.values_list(
            'image_thumb', flat=True).filter(
                classified=classified
            )[:1]

        if not Conversation.objects.conversation_exists(from_user, to_user):

            key = "{}.{}".format(*sorted([from_user.pk, to_user.pk]))
            conv = Conversation(first_user=from_user,
                            second_user=to_user,
                            key=key)
            conv.save()

        if not Message.objects.msg_clsf_exists(
                from_user, to_user, classified
            ):
            Message.objects.create(
                sender=from_user,
                recipient=to_user,
                classified=classified,
                classified_thumbnail=str(classified_thumbnail[0])
            )
        return redirect("messager:conversation_detail" , to)



@login_required
@require_http_methods(["GET"])
def make_conversations(request):
    """ A temporally view to create Conversations to users already chatted
    before Convervation model was created."""
    messages = Message.objects.all()
    for message in messages:
        from_user = message.sender
        to_user = message.recipient

        if message.conversation:
            continue
        if Conversation.objects.conversation_exists(from_user, to_user):
            key = "{}.{}".format(*sorted([from_user.pk, to_user.pk]))
            #I have deliberately not used try catch because at this step I assume
            #that every conversation must have a key. And also this method can not
            #be invoked by the normal users. So if fails, the programmer should fix
            #the undelying problem of why the conversation had no key
            message.conversation = Conversation.objects.get(key=key)
            message.save()
            continue
        else:
            key = "{}.{}".format(*sorted([from_user.pk, to_user.pk]))
            conv = Conversation(first_user=from_user, second_user=to_user, key=key)
            conv.save()

            message.conversation = conv
            message.save()

    return redirect('messager:contacts_list')


@login_required
@require_http_methods(["GET"])
def make_classifieds_as_messages(request):
    """ A temporally view to create Conversations to users already chatted
    before Convervation model was created."""
    convs = Conversation.objects.all()
    for con in convs:
        classified = Conversation.objects.get_conv_classified(con.first_user, con.second_user)

        if classified:
            try:
                classified = Classified.objects.get(id=classified[0])
            except Classified.DoesNotExist:
                continue
            else:
                classified_thumbnail = ClassifiedImages.objects.values_list(
                    'image_thumb', flat=True).filter(
                        classified=classified
                    )[:1]
                Message.objects.create(
                    sender=sender,
                    recipient=recipient,
                    classified=classified,
                    classified_thumbnail=str(classified_thumbnail)
                )
    return HttpResponse("Done!")
