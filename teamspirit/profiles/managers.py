"""Contain the managers for the models in app ``profiles``."""

from django.db import models

from teamspirit.users.models import User


class PersonalManager(models.Manager):
    """Manage the model ``Personal``."""
    # pass


class RoleManager(models.Manager):
    """Manage the model ``Role``."""
    # pass


def rename_id_file(instance, file_name):
    user = User.objects.get(personal=instance.id)
    return f"id/{user.last_name}_{user.first_name}/{file_name}"


def rename_medical_file(instance, file_name):
    user = User.objects.get(personal=instance.id)
    return f"lic/{user.last_name}_{user.first_name}/{file_name}"
