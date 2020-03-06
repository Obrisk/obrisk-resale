from django_elasticsearch_dsl import Document
from elasticsearch_dsl.connections import connections
from django.views.decorators.http import require_http_methods
from django_elasticsearch_dsl.registries import registry

from obrisk.stories.documents import StoriesDocument
from obrisk.classifieds.document import ClassifiedDocument
from obrisk.posts.documents import PostsDocument
from obrisk.qa.documents import QuestionDocument



