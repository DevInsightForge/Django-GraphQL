import graphene

from messenger.queries import ChatQuery


# Messenger Definitions
class MessengerQuery(ChatQuery, graphene.ObjectType):
    pass


# Mutations
class MessengerMutation(graphene.ObjectType):
    pass
