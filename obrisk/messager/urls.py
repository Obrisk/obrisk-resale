from django.conf.urls import url

from obrisk.messager import views

app_name = 'messager'
urlpatterns = [
    url(r'^$', views.ContactsListView.as_view(), name='contacts_list'),
    url(r'^send-message/$', views.send_message, name='send_message'),
    url(r'^receive-message/$', views.receive_message, name='receive_message'),
    url(r'^make-conversations/$', views.make_conversations, name='make_conversations'),    
    url(r'^make-classifieds/$', views.make_classifieds_as_messages, name='make_classifieds'),    
    url(r'^classified-chat/(?P<to>([^/]+))/(?P<classified>[-\w]+)/$', views.classified_chat, name='classified_chat'),
    url(r'^chat/(?P<username>([^/]+))/$', views.MessagesListView.as_view(),
        name='conversation_detail'),
]
