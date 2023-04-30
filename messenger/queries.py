import graphene
from graphql import GraphQLError

from graphql_jwt.decorators import login_required
from messenger.models import Chat

from messenger.types import BasicChatType, ChatType


class ChatListQuery(graphene.ObjectType):
    my_chats = graphene.List(
        BasicChatType,
        description="Get all available chats.",
    )

    @login_required
    def resolve_my_chats(self, info, **kwargs):
        return Chat.objects.filter(participants=info.context.user)


class ChatQuery(graphene.ObjectType):
    get_chat = graphene.Field(
        ChatType,
        chat_id=graphene.UUID(default_value=None),
        description="Get chat by id",
    )

    @login_required
    def resolve_get_chat(self, info, chat_id=None, **kwargs):
        try:
            return Chat.objects.get(participants=info.context.user, id=chat_id)
        except Chat.DoesNotExist as e:
            raise GraphQLError(f"No chat not found with id {chat_id}!") from e
