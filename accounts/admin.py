from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email')
        }),
        ('Personal info', {
            'fields': ('gender', 'birthdate', 'position')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    list_display = ('email', 'username', 'is_active', 'gender', 'birthdate', 'position')
