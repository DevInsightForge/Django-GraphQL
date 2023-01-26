import graphene
from account.schema import AuthMutation, AuthQuery


# Root Schema Definitions
class Query(AuthQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


RootSchema = graphene.Schema(query=Query, mutation=Mutation)
