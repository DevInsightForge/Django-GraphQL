import graphene
from account.schema import AccountMutation, AccountQuery


# Root Schema Definitions
class Query(AccountQuery, graphene.ObjectType):
    pass


class Mutation(AccountMutation, graphene.ObjectType):
    pass


RootSchema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
