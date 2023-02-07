from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.manager import CustomUserManager


class User(AbstractUser):
    """
    Custom user model
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    objects = CustomUserManager()
    email = models.EmailField(
        _("Email Address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d", verbose_name="Avatar Image", blank=True, null=True
    )
    phone_number = models.CharField(
        max_length=50, verbose_name="Phone Number", blank=True, null=True
    )
    birth_date = models.DateField(verbose_name="Birth Date", blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-date_joined"]
