import graphene
from graphene_django import DjangoObjectType

from messenger.models import Chat, Message


class ChatType(DjangoObjectType):
    class Meta:
        model = Chat


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
