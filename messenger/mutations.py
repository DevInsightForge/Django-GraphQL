from uuid import UUID
from graphene_django_cud.mutations.create import DjangoCreateMutation
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from messenger.models import Chat, Message
from messenger.types import BasicChatType, ChatType, MessageType


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

    # @classmethod
    # @login_required
    # def mutate(cls, root, info, input):
    #     user = info.context.user
    #     print(user)
    #     print(input)
    #     return None
    # try:
    #     obj, _ = cls._meta.model.objects.update_or_create(input)
    #     return_data = {cls._meta.return_field_name: obj}
    #     return cls(**return_data)
    # except Exception as e:
    #     raise ValueError(e) from e


# class NewMessageMutation(DjangoCreateMutation):
#     message = graphene.Field(MessageType)

#     class Meta:
#         model = Message
#         type_name = "MessageInput"
#         return_field_name = "message"
#         fields = ("content",)
#         # exclude_fields = ("messages",)
#         # many_to_many_extras = {
#         #     "participants": {
#         #         "add": {"type": "ID"},
#         #     },
#         # }

#     # @classmethod
#     # @login_required
#     # def mutate(cls, root, info, input):
#     #     input["user"] = info.context.user
#     #     try:
#     #         obj, _ = cls._meta.model.objects.update_or_create(input)
#     #         return_data = {cls._meta.return_field_name: obj}
#     #         return cls(**return_data)
#     #     except Exception as e:
#     #         raise ValueError(e) from e
