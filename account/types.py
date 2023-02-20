from graphene_django import DjangoObjectType
from account.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
        )
