import graphene
from account.schema import AccountMutation, AccountQuery
from messenger.schema import MessengerQuery


# Root Schema Definitions
class Query(MessengerQuery, AccountQuery, graphene.ObjectType):
    pass


class Mutation(AccountMutation, graphene.ObjectType):
    pass


RootSchema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
