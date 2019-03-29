from django.conf.urls import url

from obrisk.messager import views

app_name = 'messager'
urlpatterns = [
    url(r'^$', views.ContactsListView.as_view(), name='contacts_list'),
    url(r'^messages/$', views.MessagesListView.as_view(), name='messages_list'),
    url(r'^send-message/$', views.send_message, name='send_message'),
    url(r'^receive-message/$',
        views.receive_message, name='receive_message'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.ConversationListView.as_view(),
        name='conversation_detail'),
]
