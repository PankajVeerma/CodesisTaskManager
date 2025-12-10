from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "name", "is_active", "is_staff", "is_verified")
    list_filter = ("is_staff", "is_active", "is_verified", "groups")
    ordering = ("email",)

    # Fields visible when editing a user
    fieldsets = (
        ("Login Credentials", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "phone", "dob", "gender")}),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser", "is_verified")}),
        ("Groups", {"fields": ("groups", "user_permissions")}),
    )

    # Fields for Add User page
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email", "name")

admin.site.register(User, CustomUserAdmin)
