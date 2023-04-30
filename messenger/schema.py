import graphene

from messenger.mutations import NewChatMutation, NewMessageMutation
from messenger.queries import ChatListQuery, ChatQuery


# Messenger Definitions
class MessengerQuery(ChatListQuery, ChatQuery, graphene.ObjectType):
    pass


# Mutations
class MessengerMutation(graphene.ObjectType):
    create_chat = NewChatMutation.Field(
        description="Create a new chat with participants"
    )
    # deleteChat
    send_message = NewMessageMutation.Field(description="Send message to a chat")
    # deleteMessage
