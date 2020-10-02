"""Contain the models related to the app ``users``."""

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from teamspirit.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    username = models.EmailField(default=email)
    first_name = models.CharField(
        max_length=30,
        verbose_name=_("first name")
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name=_("last name")
    )
    personal = models.ForeignKey(
        to='profiles.Personal',
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.upper()}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"email": self.email})
