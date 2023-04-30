import graphene
import graphql_jwt

from account.mutations import CreateUserMutation, UserInformationMutation
from account.queries import UserQuery, UsersQuery


# Auth Definitions
class AccountQuery(UserQuery, UsersQuery, graphene.ObjectType):
    pass


# Mutations
class AccountMutation(graphene.ObjectType):
    sign_up = CreateUserMutation.Field(
        description="Register user and obtain new JWT Token"
    )
    sign_in = graphql_jwt.ObtainJSONWebToken.Field(description="Obtain new JWT Token")
    update_user_information = UserInformationMutation.Field(
        description="Add information for user"
    )
