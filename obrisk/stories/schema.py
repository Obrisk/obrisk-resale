import graphene

from graphene_django.types import DjangoObjectType

from obrisk.stories.models import Stories
from obrisk.helpers import paginate_data


class StoriesType(DjangoObjectType):
    """DjangoObjectType to acces the Stories model."""
    count_thread = graphene.Int()
    count_likers = graphene.Int()

    class Meta:
        model = Stories

    def resolve_count_thread(self, info, **kwargs):
        return self.get_thread().count()

    def resolve_count_likers(self, info, **kwargs):
        return self.liked_stories.count()


class StoriesPaginatedType(graphene.ObjectType):
    """A paginated type generic object to provide pagination to the stories
    graph."""
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(StoriesType)


class StoriesQuery(object):
    all_stories = graphene.List(StoriesType)
    paginated_stories = graphene.Field(StoriesPaginatedType, page=graphene.Int())
    stories = graphene.Field(StoriesType, uuid_id=graphene.String())

    def resolve_all_stories(self, info, **kwargs):
        return Stories.objects.filter(reply=False)

    def resolve_paginated_stories(self, info, page):
        """Resolver functions to query the objects and turn the queryset into
        the PaginatedType using the helper function"""
        page_size = 30
        qs = Stories.objects.filter(reply=False)
        return paginate_data(qs, page_size, page, StoriesPaginatedType)

    def resolve_stories(self, info, **kwargs):
        uuid_id = kwargs.get('uuid_id')

        if uuid_id is not None:
            return Stories.objects.get(uuid_id=uuid_id)

        return None
