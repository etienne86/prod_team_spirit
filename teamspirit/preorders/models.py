"""Contain the models related to the app ``preorders``."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from teamspirit.catalogs.models import Product
from teamspirit.preorders.managers import ShoppingCartLineManager, ShoppingCartManager  # noqa
from teamspirit.users.models import User


class ShoppingCart(models.Model):
    """Contain shopping cart information."""

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    is_open = models.BooleanField(
        default=True,
    )
    objects = ShoppingCartManager()

    def __str__(self):
        return f"Pré-commande pour {self.user}"

    def get_cart_amount(self):
        queryset = ShoppingCartLine.objects.filter(shopping_cart=self)
        return sum([item.get_line_amount() for item in queryset])


class ShoppingCartLine(models.Model):
    """Contain shopping cart information."""

    class Size(models.TextChoices):
        EXTRASMALL = 'XS', 'XS'
        SMALL = 'S', 'S'
        MEDIUM = 'M', 'M'
        LARGE = 'L', 'L'
        EXTRALARGE = 'XL', 'XL'

    shopping_cart = models.ForeignKey(
        to=ShoppingCart,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Quantité',
        default=1,
        null=False,
        blank=False,
    )
    size = models.CharField(
        max_length=2,
        choices=Size.choices,
        verbose_name='Taille',
        null=False,
        blank=False,
    )

    objects = ShoppingCartLineManager()

    def get_line_amount(self):
        return self.product.price * self.quantity
