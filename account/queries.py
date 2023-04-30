import graphene

from graphql_jwt.decorators import login_required
from graphql import GraphQLError

from account.types import UserType
from account.models import User


class UserQuery(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        user_id=graphene.UUID(default_value=None),
        description="Get user information by using user's ID. Defaults to self.",
    )

    @login_required
    def resolve_user(self, info, **kwargs):
        user_id = info.context.user.id
        if kwargs["user_id"]:
            if not info.context.user.is_staff or not info.context.user.is_superuser:
                raise GraphQLError("You do not have permission to view other users")

            user_id = kwargs["user_id"]

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            raise GraphQLError(f"No user not found with id {user_id}!") from e


class UsersQuery(graphene.ObjectType):
    users = graphene.List(UserType, description="Get all user's information")

    @login_required
    def resolve_users(self, info, **kwargs):
        if not info.context.user.is_staff or not info.context.user.is_superuser:
            raise GraphQLError("You do not have permission to view other users")
        return User.objects.all()
