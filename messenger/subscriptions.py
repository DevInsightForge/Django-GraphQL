import channels_graphql_ws
import graphene
from graphql import GraphQLError
from channels.db import database_sync_to_async

from messenger.models import Chat
from messenger.types import MessageType


class OnNewChatMessage(channels_graphql_ws.Subscription):
    """Subscription triggers on a new chat message."""

    message = graphene.Field(MessageType)

    class Arguments:
        """Subscription arguments."""

        chatroom = graphene.String()

    async def subscribe(self, info, *args, **kwargs):
        # access auth user
        chat_id = kwargs.get("chatroom")
        user = info.context.channels_scope["user"]
        """Client subscription handler."""

        try:
            chat = await database_sync_to_async(Chat.objects.get)(
                participants=user, id=chat_id
            )
        except Chat.DoesNotExist as e:
            raise GraphQLError(f"No chat not found with id {chat_id}!") from e

        # Specify the subscription group client subscribes to.
        print(chat)
        return [f"{chat.id}"]

    def publish(self, info, chatroom=None):
        """Called to prepare the subscription notification message."""

        # The `self` contains payload delivered from the `broadcast()`.
        message = self["message"]

        # Method is called only for events on which client explicitly
        # subscribed, by returning proper subscription groups from the
        # `subscribe` method. So he either subscribed for all events or
        # to particular chatroom.
        assert chatroom is None or chatroom == str(message.chat.id)

        return OnNewChatMessage(message=message)

    @classmethod
    def new_chat_message(cls, message):
        """Auxiliary function to send subscription notifications.

        It is generally a good idea to encapsulate broadcast invocation
        inside auxiliary class methods inside the subscription class.
        That allows to consider a structure of the `payload` as an
        implementation details.
        """
        cls.broadcast_sync(
            group=str(message.chat.id),
            payload={"message": message},
        )
