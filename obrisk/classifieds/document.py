from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer
from obrisk.classifieds.models import Classified, ClassifiedTags
# from elasticsearch_dsl import analysis


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=[
        "lowercase",
        "stop",
        "snowball"
        # analysis.token_filter("custom_nGram",
        #                      "nGram",
        #                      min_gram=3,
        #                      max_gram=3)
    ],

    char_filter=["html_strip"]
)


@registry.register_document
class ClassifiedDocument(Document):
    details = fields.TextField(
                analyzer=html_strip,
                fields={'raw': fields.KeywordField()}
            )

    tags = fields.NestedField(properties={
                'name': fields.TextField(analyzer=html_strip),
            })

    class Index:

        name = 'classifieds'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Classified
        fields = [
            'title',
            'price',
        ]


@registry.register_document
class ClassifiedTagsDocument(Document):

    name = fields.NestedField(properties={
        'name': fields.TextField(analyzer=html_strip),
        })

    class Index:

        name = 'classified_tags'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = ClassifiedTags
