"""Contain the models related to the app ``core``."""


from django.db import models


class Address(models.Model):
    """Contain address fields."""

    label_first = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        verbose_name='Numéro et voie',
        default=''
    )
    label_second = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Complément',
        default=''
    )
    postal_code = models.CharField(
        max_length=5,
        blank=False,
        null=True,
        verbose_name='Code postal',
        default=''
    )
    city = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        verbose_name='Ville',
        default=''
    )
    country = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        verbose_name='Pays',
        default=''
    )

    def __str__(self):
        if self.label_second:
            return f"{self.label_first}\n{self.label_second}\n" + \
                f"{self.postal_code}\n{self.city}\n{self.country}"
        return f"{self.label_first}\n" + \
            f"{self.postal_code}\n{self.city}\n{self.country}"


class Location(models.Model):
    """Name an address."""

    name = models.CharField(
        max_length=100,
        verbose_name="Libellé du lieu",
        unique=True
    )
    address = models.OneToOneField(
        to=Address,
        on_delete=models.CASCADE
    )
