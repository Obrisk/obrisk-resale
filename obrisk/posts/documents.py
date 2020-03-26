from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer

from obrisk.posts.models import Post, PostTags


html_strip = analyzer(
        'html_strip',
        tokenizer="standard",
        filter=["lowercase", "stop", "snowball"],
        char_filter=["html_strip"]
)


@registry.register_document
class PostsDocument(Document):
    content = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )
    tags = fields.NestedField(properties={
                'name': fields.TextField(analyzer=html_strip),
            })

    class Index:

        name = 'posts'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Post
        fields = [
            'title',
        ]


@registry.register_document
class PostTagsDocument(Document):

    name = fields.TextField(analyzer=html_strip)

    class Index:

        name = 'post_tags'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = PostTags
