from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.urls import reverse

from slugify import slugify
from obrisk.messager.models import Message
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

class ConversationListView(LoginRequiredMixin, ListView):
    """CBV to render the inbox, showing a specific conversation with a given
    user, who requires to be active too."""

    model = Message
    paginate_by = 100
    template_name = "messager/message_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = self.kwargs["username"]
        return context

    def get(self, *args, **kwargs):
        url = str('/ws/messages/')
        if self.get_queryset() == url :
            messages.error(self.request, 
            "Hello, it looks like you are trying to do something suspicious. \
            Our system has stopped you from doing so and this information has been recorded.\
            If similar actions are repeated several times, then your account will be blocked!")
            return redirect('messager:contacts_list')
        else:
            return super(ConversationListView, self).get(*args, **kwargs)


    def get_queryset(self):     
        try:              
            active_user = get_user_model().objects.get(username=self.kwargs["username"])
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