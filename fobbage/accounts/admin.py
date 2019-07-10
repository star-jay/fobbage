from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm as BaseAdminPasswordChangeForm
)
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User


class AdminPasswordChangeForm(BaseAdminPasswordChangeForm):
    class Meta:
        fields = ['password1', 'password2']


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ("last_name",)
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm


admin.site.register(User, UserAdmin)
