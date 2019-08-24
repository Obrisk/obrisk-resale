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

from slugify import slugify
from obrisk.classifieds.models import Classified
from obrisk.messager.models import Message, Conversation
from obrisk.helpers import ajax_required


class ContactsListView(LoginRequiredMixin, ListView):
    """This CBV is used to filter the list of contacts in the user"""
    """and allow the user to select the active one before chatting"""
    model = Message
    paginate_by = 50
    template_name = "messager/contact_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        users, msgs = Message.objects.get_conversations(self.request.user)
        context['zip_list'] = zip(users, msgs)
        context['super_users'] = get_user_model().objects.filter(is_superuser=True)
        context['base_active'] = 'chat'
        return context

class MessagesListView(LoginRequiredMixin, ListView):
    """CBV to render the inbox, showing a specific conversation with a given
    user, who requires to be active too."""

    model = Message
    paginate_by = 100
    template_name = "messager/message_list.html"

    

    def get_context_data(self, *args, **kwargs):
        username=self.kwargs["username"] 
        context = super().get_context_data(*args, **kwargs)
        context['active'] = username

        try:
            active_user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            messages.error(self.request, f"Sorry, The user {username}, doesn't exist!")
            return reverse('messager:contacts_list')    
        
        classified = Conversation.objects.get_conv_classified(self.request.user, active_user)
        if classified:
            try:
                classified = Classified.objects.get(id=classified[0])
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
            messages.error(self.request, f"Hey you there, it looks like you're trying to do something bad. \
                Your account {self.request.user.username}, has been flagged, and if this happens again, you will be blocked!")
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
    message = request.POST.get('message')
    if len(message.strip()) == 0:
        return HttpResponse()

    if sender != recipient:
        #Django-channels doesn't accept group names that are chinese characters
        #This is a trivial workaround to avoid an error to happen in case the name of user is in chinese characters
        recipient.username = slugify(recipient_username)
        sender.username = slugify(request.user.username)
        msg = Message.send_message(sender, recipient, message)
        return render(request, 'messager/single_message.html',
                      {'message': msg})

    return HttpResponse()

@login_required
@ajax_required
@require_http_methods(["GET"])
def receive_message(request):
    """Simple AJAX functional view to return a rendered single message on the
    receiver side providing realtime connections."""
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
                conv = Conversation(first_user=from_user, second_user=to_user, classified=classified)
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

        if Conversation.objects.conversation_exists(from_user, to_user):
            continue            
        else:
            conv = Conversation(first_user=from_user, second_user=to_user)
            conv.save()

    return redirect('messager:contacts_list')

