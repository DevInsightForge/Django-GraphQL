from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from graphql_jwt.refresh_token.models import RefreshToken as AbstractRefreshToken
from phonenumber_field.modelfields import PhoneNumberField

from account.manager import CustomUserManager


class User(AbstractUser):
    """
    Custom user model
    """

    id = models.UUIDField(
        _("Id"),
        primary_key=True,
        default=uuid4,
    )

    email = models.EmailField(
        _("Email Address"),
        unique=True,
        help_text=_("Email address which acts as unique identifier."),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    objects = CustomUserManager()

    # email = models.EmailField(
    #     _("Email Address"),
    #     unique=True,
    #     error_messages={
    #         "unique": _("A user with that email already exists."),
    #     },
    # )

    # avatar = models.ImageField(
    #     upload_to="avatars/%Y/%m/%d", verbose_name="Avatar Image", blank=True, null=True
    # )
    # phone_number = PhoneNumberField(
    #     max_length=20, verbose_name="Phone Number", blank=True, null=True
    # )
    # birth_date = models.DateField(verbose_name="Birth Date", blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.email

    def clean(self) -> None:
        self.email = self.__class__.objects.normalize_email(self.email)


class UserRefreshToken(AbstractRefreshToken):
    class Meta:
        proxy = True
        verbose_name = "Refresh Token"
