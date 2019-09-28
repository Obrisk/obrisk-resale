#Please ignore pylint hint on Classified.DoesNotExist
#This code is valid

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.urls import reverse
from django.db.models import Q
from django.db.models import OuterRef, Subquery, Case, When, Value, IntegerField
import time

import os
import base64
import datetime
import oss2

from slugify import slugify
from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.messager.models import Message, Conversation
from obrisk.helpers import ajax_required, bucket, bucket_name


class ContactsListView(LoginRequiredMixin, ListView):
    """This CBV is used to filter the list of contacts in the user"""
    """and allow the user to select the active one before chatting"""
    model = Message
    paginate_by = 50
    template_name = "messager/contact_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['convs'] = Conversation.objects.get_conversations(self.request.user).annotate(
                    time = Subquery (
                        Message.objects.filter(
                            conversation=OuterRef('pk'),
                        ).values('timestamp')[:1]
                    ), 
                    last_msg = Subquery (
                        Message.objects.filter(
                            conversation=OuterRef('pk'),
                        ).values('message')[:1]
                    ),
                    img = Subquery (
                        Message.objects.filter(
                            conversation=OuterRef('pk'),
                        ).values('image')[:1]
                    ),
                    attachment = Subquery (
                        Message.objects.filter(
                            conversation=OuterRef('pk'),
                        ).values('attachment')[:1]
                    ),
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
                ).order_by('-time')

        #users, msgs = Message.objects.get_conversations(self.request.user)
        #context['zip_list'] = zip(users, msgs) 
        context['super_users'] = get_user_model().objects.filter(is_superuser=True)
        context['base_active'] = 'chat'

        if context['convs'][0].first_user == self.request.user:
            context['active'] = context['convs'][0].second_user.username
        else:
            context['active'] = context['convs'][0].first_user.username
        return context

class MessagesListView(LoginRequiredMixin, ListView):
    """CBV to render the inbox, showing a specific conversation with a given
    user, who requires to be active too."""

    model = Message
    paginate_by = 100
    template_name = "messager/message_list.html"

    def get(self, *args, **kwargs):
        url = str('/ws/messages/')
        if self.get_queryset() == url :
            messages.error(self.request, 
            f"Hello, It looks like you are trying to do something bad. \
            Your account {self.request.user.username}, has been flagged. \
            If similar actions happen again, this account will be blocked!")
            return redirect('messager:contacts_list')
        else:
            return super(MessagesListView, self).get(*args, **kwargs)


    def get_context_data(self, *args, **kwargs): 
        context = super().get_context_data(*args, **kwargs)
        context['active'] = self.kwargs["username"]

        try:
            active_user = get_user_model().objects.get(username=self.kwargs["username"])
        except get_user_model().DoesNotExist:
            return context    
        
        classified = Conversation.objects.get_conv_classified(self.request.user, active_user)
        if classified:
            try:
                classified = Classified.objects.annotate (
                    image_thumb = Subquery (
                        ClassifiedImages.objects.filter(
                            classified=OuterRef('pk'),
                        ).values(
                            'image_thumb'
                        )[:1]
                    )
                ).get(id=classified[0])
            except Classified.DoesNotExist:
                return context
            else: 
                context['classified'] = classified
        return context


    def get_queryset(self):    
        try:               
            active_user = get_user_model().objects.get(username=self.kwargs["username"])
            
            #When I have fully migrated to the conversation model design this condition becomes important
            #if Conversation.objects.conversation_exists(self.request.user, active_user):
            
            #Below is called only when the conversation is opened thus mark all msgs as read.
            #In the near future implement it to query only last 100 messages, and update last few images.
            Message.objects.filter(sender=active_user, recipient=self.request.user).update(unread=False)         
            return Message.objects.get_msgs(active_user, self.request.user)      
            
        except get_user_model().DoesNotExist:
            return reverse('messager:contacts_list')   

         
@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    sender = request.user
    recipient_username = request.POST.get('to')
    try:
        recipient = get_user_model().objects.get(username=recipient_username)
    except get_user_model().DoesNotExist:
        return HttpResponseNotFound("The user account appears to not exist or it has been freezed!")

    #Django-channels doesn't accept group names that are chinese characters
    #This is a trivial workaround to avoid an error to happen in case the name of user is in chinese characters
    recipient.username = slugify(recipient_username)
    sender.username = slugify(request.user.username)

    message = request.POST.get('message')
    image = request.POST.get('image')
    attachment = request.POST.get('attachment')
    img_preview=None

    if not message and not image and not attachment:
        return HttpResponse()
    
    if image:
        if image.startswith(f'messages/{sender.username}/{recipient.username}') == False:
            print(f'messages/{sender.username}/{recipient.username}')             
            image = None

        else:
            d = str(datetime.datetime.now())
            img_preview = "messages/" + slugify(str(request.user.username)) + slugify(str(recipient_username)) + "/preview/" + "prv-" + d 
            style1 = 'image/resize,m_fill,h_250,w_250'

            try:
                process1 = "{0}|sys/saveas,o_{1},b_{2}".format(style1,
                                                            oss2.compat.to_string(base64.urlsafe_b64encode(
                                                                oss2.compat.to_bytes(img_preview))),
                                                            oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
                bucket.process_object(image, process1)
            except:
                image = None
                img_preview = None
    
    if message:
        if len(message.strip()) == 0:
            return HttpResponse()
  
    if sender != recipient:
        msg = Message.send_message(sender, recipient, message,
                            image=image, img_preview=img_preview, attachment=attachment)
        
        return render(request, 'messager/single_message.html', {'message': msg})

    return HttpResponse()

@login_required
@ajax_required
@require_http_methods(["GET"])
def receive_message(request):
    """Simple AJAX functional view to return a rendered single message on the
    receiver side providing realtime connections."""
    try:
        message_id = request.GET.get('message_id')
        message = Message.objects.get(pk=message_id)
    except:
        time.sleep(5)
        message_id = request.GET.get('message_id')
        message = Message.objects.get(pk=message_id)
    return render(request,
                  'messager/single_message.html', {'message': message})


@login_required
@require_http_methods(["GET"])
def classified_chat(request, to, classified):
    """ Create a Conversation object btn 2 users """
    try:
        to_user = get_user_model().objects.get(username=to)
        from_user = request.user
    except get_user_model().DoesNotExist:
        messages.error(request, f"Sorry, The user {to}, doesn't exist!")
        return redirect('messager:contacts_list')

    if Conversation.objects.conversation_exists(from_user, to_user):
        return redirect("messager:conversation_detail" , to)
    else:
        try:
            classified = Classified.objects.get(id=classified)
        except Classified.DoesNotExist:
            #This error message assumes that the classifieds items are never deleted completely.
            #If the user reaches here then he/she was playing with url parameters.
            messages.error(request, f"Hey you there, it looks like you're trying to do something bad. \
                Your account { from_user}, has been flagged, and if this happens again, you will be blocked!")
            return redirect('messager:contacts_list')  
        
        else:  
            #This condition assumes classified parameter should never be null.
            if classified.user == to_user:
                key = "{}.{}".format(*sorted([from_user.pk, to_user.pk]))
                conv = Conversation(first_user=from_user,
                                second_user=to_user,
                                key=key,
                                classified=classified)
                conv.save()
                return redirect('messager:conversation_detail', to)
            else:
                messages.error(request, f"Hey you there, it looks like you're trying to do something bad. \
                    Your account { from_user}, has been flagged, and if this happens again, you will be blocked!")
                return redirect('messager:contacts_list')
            


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


