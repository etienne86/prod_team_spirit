"""Contain the models related to the app ``catalogs``."""

from django.db import models

from teamspirit.catalogs.managers import CatalogManager, ProductManager


class Catalog(models.Model):
    """Contain catalog information."""

    name = models.CharField(
        max_length=50,
        verbose_name='Nom du catalogue',
        null=False,
        blank=False,
        default='(catalogue sans nom)',
    )

    objects = CatalogManager()

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """Contain product information."""

    name = models.CharField(
        max_length=50,
        verbose_name='Article',
        null=False,
        blank=False,
        default='(produit sans nom)',
    )
    image = models.FileField(
        null=True,
        blank=True,
        verbose_name='Photo',
        upload_to='produits/',
    )
    is_available = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name='Produit disponible ?',
    )
    is_free = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name='Produit offert ?',
    )
    price = models.IntegerField(
        verbose_name='Prix',
        null=True,
        blank=True,
        default=0,
    )
    catalog = models.ForeignKey(
        to=Catalog,
        on_delete=models.CASCADE,
        null=False,
    )

    def __str__(self):
        return f"{self.name}"

    objects = ProductManager()
