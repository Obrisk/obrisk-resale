from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.connections import connections
from obrisk.stories.models import Stories


connections.create_connection()


@registry.register_document
class StoriesDocument(Document):

    class Index:
        name = 'stories'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Stories
        fields = [
            'content',
        ]
