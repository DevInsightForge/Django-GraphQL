import graphene

from messenger.mutations import NewChatMutation
from messenger.queries import ChatListQuery, ChatQuery


# Messenger Definitions
class MessengerQuery(ChatListQuery, ChatQuery, graphene.ObjectType):
    pass


# Mutations
class MessengerMutation(graphene.ObjectType):
    newChat = NewChatMutation.Field()
