from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.connections import connections
from obrisk.stories.models import Stories, StoryTags

from elasticsearch_dsl import analyzer
html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

connections.create_connection()


@registry.register_document
class StoriesDocument(Document):

    tags = fields.NestedField(properties={
                'name': fields.TextField(analyzer=html_strip),
            })

    class Index:
        name = 'stories'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Stories
        fields = [
            'content',
        ]


@registry.register_document
class StoryTagsDocument(Document):

    name = fields.TextField(analyzer=html_strip)

    class Index:

        name = 'story_tags'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = StoryTags

