import graphene
from django.contrib.auth import get_user_model
from graphene_django_cud.mutations.create import DjangoCreateMutation
from account.models import User
from account.types import UserType
from graphql_jwt.mixins import ObtainJSONWebTokenMixin
from graphql_jwt.decorators import token_auth
from account.forms import SignupForm
from graphql import GraphQLError


class CreateUserMutation(ObtainJSONWebTokenMixin, DjangoCreateMutation):
    user = graphene.Field(UserType)

    class Meta:
        model = User
        fields = (
            "email",
            # "first_name",
            # "last_name",
            # "avatar",
        )
        custom_fields = {
            "password1": graphene.String(required=True),
            "password2": graphene.String(required=True),
        }

    @classmethod
    def mutate(cls, root, info, input):
        input_files = {
            key: value for key, value in input.items() if not isinstance(value, str)
        }

        form = SignupForm(input, input_files)

        if form.is_valid():
            form.save()
            kwargs = {
                "password": form.data["password1"],
                get_user_model().USERNAME_FIELD: form.data[
                    get_user_model().USERNAME_FIELD
                ],
            }
            return cls.authorize_user(root, info, **kwargs)

        form_errors = {
            key: value[0] for key, value in form.errors.items() if key in form.errors
        }
        raise GraphQLError(
            message="ValidationError: Failed to create new user",
            extensions={"inputErrors": form_errors},
        )

    @classmethod
    @token_auth
    def authorize_user(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)
