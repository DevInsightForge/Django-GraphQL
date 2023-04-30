import graphene
from graphene_django import DjangoObjectType

from messenger.models import Chat, Message


class ChatType(DjangoObjectType):
    class Meta:
        model = Chat


class BasicChatType(DjangoObjectType):
    class Meta:
        model = Chat
        exclude = (
            "participants",
            "messages",
        )


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
