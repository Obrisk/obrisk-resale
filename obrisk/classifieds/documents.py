from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer
from obrisk.classifieds.models import Classified
# from elasticsearch_dsl import analysis

from elasticsearch_dsl.connections import connections
from django_elasticsearch_dsl import Document, Index


# Create a connection to ElasticSearch
#connections.create_connection()

# reference elasticsearch doc for default settings here
#classified.settings(
#    number_of_shards=1,
#    number_of_replicas=0
#)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=[
        "lowercase",
        "stop",
        "snowball"
    ],
    char_filter=["html_strip"]
)

@registry.register_document
class ClassifiedDocument(Document):
    title = fields.TextField(
                analyzer=html_strip,
                fields={'raw': fields.KeywordField()}
            )

    details = fields.TextField(
                analyzer=html_strip,
                fields={'raw': fields.KeywordField()}
            )

    tags = fields.ObjectField(properties={
            'name': fields.TextField(
                    analyzer=html_strip,
                    fields={'raw': fields.KeywordField()}
                )
        })

    english_address = fields.TextField(
                analyzer=html_strip,
                fields={'raw': fields.KeywordField()}
            )

    class Index:
        # Name of the Elasticsearch index
        name = 'classifieds'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Classified
