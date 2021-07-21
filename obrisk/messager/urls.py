from django.conf.urls import url

from obrisk.messager import views

app_name = 'messager'
urlpatterns = [
    url(r'^$',
        views.ContactsListView.as_view(),
        name='contacts_list'
    ),
    url(r'^send-message/$',
        views.send_message,
        name='send_message'
    ),
    url(r'^receive-message/$',
        views.receive_message,
        name='receive_message'
    ),
    url(r'^wsguatpotlfwccdi/send-wx-template/(?P<user>([^/]+))/(?P<last_msg>[-\w]+)/(?P<sender>[-\w]+)/(?P<time>[-\w]+)/$',
        views.test_send_wxtemplate,
        name='send_wxtemplate'
    ),
    url(r'^wsguatpotlfwccdi/test-unread-messages/([-\w]+)/$',
        views.test_unread_messages,
        name='unread_messages'
    ),
    url(r'^classified-chat/(?P<to>([^/]+))/(?P<classified>[-\w]+)/$',
        views.classified_chat,
        name='classified_chat'
    ),
    url(r'^chat/(?P<username>([^/]+))/$',
        views.messagesView,
        name='conversation_detail'
    ),
]
