import graphene

from django.contrib.auth import get_user_model
from graphene_django_cud.mutations.create import DjangoCreateMutation
from account.models import User, UserInformationModel
from account.types import UserType
from graphql_jwt.mixins import ObtainJSONWebTokenMixin
from graphql_jwt.decorators import token_auth, login_required
from account.forms import SignupForm
from graphql import GraphQLError


class UserInformationMutation(DjangoCreateMutation):
    class Meta:
        model = UserInformationModel
        type_name = "UserInformationInput"
        return_field_name = "updatedUserInformation"
        exclude_fields = (
            "id",
            "user",
        )
        field_types = {
            "gender": graphene.Enum.from_enum(UserInformationModel.GenderChoices)(),
        }

    @classmethod
    @login_required
    def mutate(cls, root, info, input):
        input["user"] = info.context.user
        try:
            obj, _ = cls._meta.model.objects.update_or_create(input)
            return_data = {cls._meta.return_field_name: obj}
            return cls(**return_data)
        except Exception as e:
            raise ValueError(e) from e
