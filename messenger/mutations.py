import graphene

from uuid import UUID
from graphene_django_cud.mutations.create import DjangoCreateMutation
from graphene_django_cud.mutations.delete import DjangoDeleteMutation
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from messenger.models import Chat, Message
from messenger.subscriptions import OnNewChatMessage
from messenger.types import BasicChatType, MessageType


class NewChatMutation(DjangoCreateMutation):
    chat = graphene.Field(BasicChatType)

    class Meta:
        model = Chat

    @classmethod
    @login_required
    def before_mutate(cls, root, info, input):
        if not len(input["participants"]):
            raise GraphQLError("No participants were added!")
            # Convert strings to UUIDv4 objects
        participants = [
            p if isinstance(p, UUID) else UUID(p) for p in input["participants"]
        ]
        # Insert user ID at the beginning of the participants list
        participants.insert(0, info.context.user.id)
        # Return updated participants list with input
        input["participants"] = participants
        return input


class DeleteChatMutation(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            obj = Chat.objects.get(pk=kwargs["id"])
            obj.delete()
            return cls(deleted=True)
        except Chat.DoesNotExist as e:
            return cls(deleted=False)


class NewMessageMutation(DjangoCreateMutation):
    message = graphene.Field(MessageType)

    class Meta:
        model = Message
        type_name = "NewMessageInput"
        exclude_fields = ("sender",)
        auto_context_fields = {"sender": "user"}
        foreign_key_extras = {"chat": {"type": "ID"}}

    @classmethod
    @login_required
    def validate(cls, root, info, input):
        if not input["content"]:
            raise GraphQLError("No message content was provided!")
        try:
            Chat.objects.get(participants=info.context.user, id=input["chat"])
        except Chat.DoesNotExist as e:
            raise GraphQLError(f"No chat not found with id {input['chat']}!") from e

    @classmethod
    def after_mutate(cls, root, info, input, obj, return_data):
        # Notify subscribers.
        OnNewChatMessage().new_chat_message(message=obj)


class DeleteMessageMutation(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            obj = Message.objects.get(pk=kwargs["id"])
            obj.delete()
            return cls(deleted=True)
        except Message.DoesNotExist as e:
            return cls(deleted=False)
