"""Contain the models related to the app ``profiles``."""

from django.db import models, transaction

from teamspirit.core.models import Address
from teamspirit.profiles.managers import (
    PersonalManager,
    RoleManager,
    rename_id_file,
    rename_medical_file,
)
from teamspirit.users.models import User


class Personal(models.Model):
    """Contain personal information."""

    phone_number = models.CharField(
        max_length=20,
        verbose_name='Téléphone',
        null=True,
        blank=False,
        default='',
    )
    address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        null=False,
    )
    has_private_profile = models.BooleanField(
        default=False,
        verbose_name='Profil privé ?',
        help_text='Si cette case est cochée, mes informations ne seront pas '
                  'visibles par les autres adhérents.',
    )
    id_file = models.FileField(
        null=True,
        blank=True,
        verbose_name='Pièce d\'identité',
        upload_to=rename_id_file,
    )
    medical_file = models.FileField(
        null=True,
        blank=True,
        verbose_name='Certificat médical ou licence',
        upload_to=rename_medical_file,
    )

    objects = PersonalManager()

    def __str__(self):
        user = User.objects.get(personal=self.id)
        result = "Informations personnelles pour " + \
            f"{user.first_name} {user.last_name}"
        return result


class Role(models.Model):
    """Qualify user's role."""

    is_member = models.BooleanField(
        default=True,
        verbose_name="Adhérent(e) de l'association"
    )
    is_secretary = models.BooleanField(
        default=False,
        verbose_name="Secrétariat"
    )
    is_treasurer = models.BooleanField(
        default=False,
        verbose_name="Trésorerie"
    )
    is_president = models.BooleanField(
        default=False,
        verbose_name="Présidence"
    )
    is_inactive = models.BooleanField(
        default=False,
        verbose_name="Non adhérent(e)"
    )

    objects = RoleManager()

    def set_as_member(self):
        """Qualify the user as member."""
        with transaction.atomic():
            self.is_member = True
            self.is_secretary = False
            self.is_treasurer = False
            self.is_president = False
            self.is_inactive = False

    def set_as_secretary(self):
        """Qualify the user as secretary."""
        with transaction.atomic():
            self.is_member = False
            self.is_secretary = True
            self.is_treasurer = False
            self.is_president = False
            self.is_inactive = False

    def set_as_treasurer(self):
        """Qualify the user as treasurer."""
        with transaction.atomic():
            self.is_member = False
            self.is_secretary = False
            self.is_treasurer = True
            self.is_president = False
            self.is_inactive = False

    def set_as_president(self):
        """Qualify the user as president."""
        with transaction.atomic():
            self.is_member = False
            self.is_secretary = False
            self.is_treasurer = False
            self.is_president = True
            self.is_inactive = False

    def set_as_inactive(self):
        """Qualify the user as inactive."""
        with transaction.atomic():
            self.is_member = False
            self.is_secretary = False
            self.is_treasurer = False
            self.is_president = False
            self.is_inactive = True
