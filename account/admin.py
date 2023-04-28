from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.models import User, UserInformationModel


class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ("email",)
    ordering = ("-date_joined",)

    list_display = (
        "id",
        "email",
        "date_joined",
        "is_staff",
        "is_active",
    )

    list_display_links = (
        "id",
        "email",
    )

    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )

    readonly_fields = (
        "is_superuser",
        "date_joined",
        "last_login",
    )

    fieldsets = (
        (
            "Login Information",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "User Permissions",
            {
                "fields": ("is_superuser", "is_staff", "is_active"),
            },
        ),
    )

    add_fieldsets = (
        (
            "Register Information",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "User Permissions",
            {
                "classes": ("wide",),
                "fields": ("is_staff", "is_active"),
            },
        ),
    )


class UserInformationsAdmin(admin.ModelAdmin):
    model = UserInformationModel
    search_fields = ("user",)
    ordering = ("-created_at",)

    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        "created_at",
    )

    list_display_links = (
        "id",
        "user",
    )

    list_filter = (
        "user",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "created_at",
                    "updated_at",
                )
            },
        ),
        (
            "User Informations",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "phone_number",
                    "birth_date",
                    "gender",
                )
            },
        ),
    )


# Register admin models
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserInformationModel, UserInformationsAdmin)


# Removing groups from admin
admin.site.unregister(Group)
