import graphene
from account.schema import AccountMutation, AccountQuery
from messenger.schema import MessengerMutation, MessengerQuery, MessengerSubscription


# Root Schema Definitions
class Query(MessengerQuery, AccountQuery, graphene.ObjectType):
    pass


class Mutation(MessengerMutation, AccountMutation, graphene.ObjectType):
    pass


class Subscription(MessengerSubscription, graphene.ObjectType):
    pass


RootSchema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
