from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from teamspirit.users.forms import UserChangeForm, UserCreationForm
from teamspirit.users.models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = (
        "email",
        "last_name",
        "first_name",
        "is_staff",
        "is_superuser"
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ("last_name", "first_name", "email")
    ordering = ('last_name',)
