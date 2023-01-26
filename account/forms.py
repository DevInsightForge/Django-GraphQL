from django.contrib.auth.forms import UserCreationForm
from account.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "avatar",
            "birth_date",
            "phone_number",
        )
