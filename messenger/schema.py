import graphene

from messenger.mutations import NewChatMutation, NewMessageMutation
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
    # deleteChat
    send_message = NewMessageMutation.Field(description="Send message to a chat")
    # deleteMessage


class MessengerSubscription(graphene.ObjectType):
    """GraphQL subscriptions."""

    on_new_chat_message = OnNewChatMessage.Field()
