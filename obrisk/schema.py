import graphene

from obrisk.stories.schema import StoriesQuery
from obrisk.users.schema import UserQuery


class Query(StoriesQuery, UserQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
