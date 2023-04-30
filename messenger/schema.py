import graphene

from messenger.mutations import NewChatMutation, NewMessageMutation
from messenger.queries import ChatListQuery, ChatQuery


# Messenger Definitions
class MessengerQuery(ChatListQuery, ChatQuery, graphene.ObjectType):
    pass


# Mutations
class MessengerMutation(graphene.ObjectType):
    newChat = NewChatMutation.Field()
    sendMessage = NewMessageMutation.Field()
