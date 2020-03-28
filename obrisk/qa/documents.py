from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer
from obrisk.qa.models import Question, QaTags


html_strip = analyzer(
        'html_strip',
        tokenizer="standard",
        filter=["lowercase", "stop", "snowball"],
        char_filter=["html_strip"]
)


@registry.register_document
class QuestionDocument(Document):
    content = fields.TextField(
                analyzer=html_strip,
                fields={'raw': fields.KeywordField()}
            )

    class Index:
        name = 'qa'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Question


@registry.register_document
class QaTagsDocument(Document):

    name = fields.TextField(analyzer=html_strip)

    class Index:

        name = 'qa_tags'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = QaTags
