import graphene

from graphql_jwt.decorators import login_required
from messenger.models import Chat

from messenger.types import ChatType


class ChatQuery(graphene.ObjectType):
    chats = graphene.List(
        ChatType,
        description="Get all available chats.",
    )

    @login_required
    def resolve_chats(self, info, **kwargs):
        return Chat.objects.filter(participants=info.context.user)
