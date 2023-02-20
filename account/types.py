from graphene_django import DjangoObjectType
from account.models import User, UserInformationModel


class UserInformationType(DjangoObjectType):
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
        )
