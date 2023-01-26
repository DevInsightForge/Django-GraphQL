from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql import GraphQLError


class FormMutation(DjangoModelFormMutation):
    class Meta:
        abstract = True

    errors = None

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        input_files = {
            key: value for key, value in input.items() if not isinstance(value, str)
        }

        form = cls.get_form(root, info, **input, files=input_files)

        if form.is_valid():
            return cls.perform_mutate(root, info, form)

        form_errors = {
            key: value[0] for key, value in form.errors.items() if key in form.errors
        }
        raise GraphQLError(
            message="Input validation failed",
            extensions={"fieldErrors": form_errors},
        )

    @classmethod
    def perform_mutate(cls, root, info, form):
        obj = form.save()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(**kwargs)
