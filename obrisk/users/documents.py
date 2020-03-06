from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer
from obrisk.users.models import User


@registry.register_document
class UsersDocument(Document):

    class Index:
        name = 'users'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = User
        fields = [
            'username',
        ]
