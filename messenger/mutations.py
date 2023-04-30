from uuid import UUID
from graphene_django_cud.mutations.create import DjangoCreateMutation
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from messenger.models import Chat, Message


class NewChatMutation(DjangoCreateMutation):
    class Meta:
        model = Chat
        exclude_fields = ("messages",)

    @classmethod
    @login_required
    def before_mutate(cls, root, info, input):
        if len(input["participants"]):
            # Convert strings to UUIDv4 objects
            participants = [
                UUID(p) if isinstance(p, str) else p for p in input["participants"]
            ]
            # Insert user ID at the beginning of the participants list
            participants.insert(0, info.context.user.id)
            # Return updated participants list with input
            input["participants"] = participants
            return input
        else:
            raise GraphQLError("No participants were added!")


class NewMessageMutation(DjangoCreateMutation):
    class Meta:
        model = Message
        type_name = "NewMessageInput"
        exclude_fields = ("sender",)
        auto_context_fields = {"sender": "user"}
        foreign_key_extras = {"chat": {"type": "ID"}}

    @classmethod
    @login_required
    def validate(cls, root, info, input):
        print(input)
        if not input["content"]:
            raise GraphQLError("No message content was provided!")
