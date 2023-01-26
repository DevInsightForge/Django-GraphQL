# src/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.models import User


class CustomUserAdmin(UserAdmin):
    model = User
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
            "User Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "birth_date",
                    "phone_number",
                    "date_joined",
                    "last_login",
                )
            },
        ),
        ("User Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "avatar",
                    "birth_date",
                    "phone_number",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("-date_joined",)


admin.site.register(User, CustomUserAdmin)

# Removing groups from admin
admin.site.unregister(Group)
