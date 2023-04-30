import graphene
from graphene_django import DjangoObjectType
from account.models import User, UserInformationModel


class UserInformationType(DjangoObjectType):
    full_name = graphene.String()

    def resolve_full_name(self, info):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    class Meta:
        model = UserInformationModel
        convert_choices_to_enum = False
        exclude = (
            "id",
            "user",
        )


class UserType(DjangoObjectType):
    informations = UserInformationType

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "chats",
            "messages",
        )
