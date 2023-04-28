from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """

    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid4,
    )

    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Email address which acts as unique identifier."),
        error_messages={
            "unique": _("A user with this email already exists."),
        },
    )

    date_joined = models.DateTimeField(
        _("date joined"),
        auto_now_add=True,
    )

    last_login = models.DateTimeField(
        _("last login"),
        auto_now=True,
    )

    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_("Designates whether the user has superuser permissions."),
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.email

    def clean(self) -> None:
        self.email = self.__class__.objects.normalize_email(self.email)


class UserInformationModel(models.Model):
    """
    Model to store user basic information
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="informations",
    )

    first_name = models.CharField(
        _("first name"),
        max_length=254,
    )

    last_name = models.CharField(
        _("last name"),
        max_length=254,
    )

    phone_number = models.CharField(
        _("phone number"),
        max_length=50,
        blank=True,
        null=True,
    )

    avatar = models.ImageField(
        _("avatar image"),
        upload_to="avatars/%Y/%m/%d",
        blank=True,
        null=True,
    )

    birth_date = models.DateField(
        _("birth date"),
        blank=True,
        null=True,
    )

    class GenderChoices(models.TextChoices):
        male = "male", _("Male")
        female = "female", _("Female")
        other = "other", _("Other")

    gender = models.CharField(
        _("choose gender"),
        max_length=10,
        blank=True,
        null=True,
        choices=GenderChoices.choices,
    )

    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        editable=False,
    )

    class Meta:
        verbose_name = _("User Information")

    def __str__(self):
        return f"{self.user}'s informations"
