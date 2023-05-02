import graphene

from messenger.mutations import (
    DeleteChatMutation,
    DeleteMessageMutation,
    NewChatMutation,
    NewMessageMutation,
)
from messenger.queries import ChatListQuery, ChatQuery
from messenger.subscriptions import OnNewChatMessage


# Messenger Definitions
class MessengerQuery(ChatListQuery, ChatQuery, graphene.ObjectType):
    pass


# Mutations
class MessengerMutation(graphene.ObjectType):
    create_chat = NewChatMutation.Field(
        description="Create a new chat with participants"
    )
    delete_chat = DeleteChatMutation.Field(description="Delete a chat by id")
    send_message = NewMessageMutation.Field(description="Send message to a chat")
    delete_message = DeleteMessageMutation.Field(description="Delete a message by id")


class MessengerSubscription(graphene.ObjectType):
    """GraphQL subscriptions."""

    new_chat_message = OnNewChatMessage.Field()
