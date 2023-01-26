from graphene_django import DjangoObjectType, registry
from account.models import User
from graphene import Node


class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
        exclude = (
            "password",
            "is_superuser",
        )
