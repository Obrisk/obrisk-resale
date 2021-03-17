from django.conf.urls import url

from obrisk.search import views

app_name = 'search'
urlpatterns = [
    url(r'^$', views.SearchListView.as_view(), name='results'),
    url(r'^results$', views.all_search, name='elastic_results'),
    url(r'^suggestions/$', views.get_suggestions, name='suggestions'),
]
