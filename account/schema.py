import graphene
import graphql_jwt
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from account.models import User
from account.mutations import CreateUserMutation, UserInformationMutation
from account.types import UserType


# Auth Definitions
class AccountQuery(graphene.ObjectType):

    user = graphene.Field(
        UserType,
        user_id=graphene.UUID(default_value=None),
        description="Get user information by using user's ID. Defaults to self.",
    )
    users = graphene.List(UserType, description="Get all user's information")

    @login_required
    def resolve_user(self, info, **kwargs):
        user_id = kwargs["user_id"]
        if user_id is None:
            return User.objects.get(id=info.context.user.id)
        if not info.context.user.is_staff or not info.context.user.is_superuser:
            raise GraphQLError("You do not have permission to view other users")
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            raise GraphQLError(f"No user not found with id {user_id}!") from e

    @login_required
    def resolve_users(self, info, **kwargs):
        if not info.context.user.is_staff or not info.context.user.is_superuser:
            raise GraphQLError("You do not have permission to view other users")
        return User.objects.all()


# Mutations
class AccountMutation(graphene.ObjectType):
    sign_up = CreateUserMutation.Field(
        description="Register user and obtain new JWT Token"
    )
    sign_in = graphql_jwt.ObtainJSONWebToken.Field(description="Obtain new JWT Token")
    sign_out = graphql_jwt.DeleteJSONWebTokenCookie.Field(
        description="Revoke a JWT Token"
    )
    refresh = graphql_jwt.Refresh.Field(description="Obtain Refresh JWT Token")

    update_user_information = UserInformationMutation.Field(
        description="Add information for user"
    )
