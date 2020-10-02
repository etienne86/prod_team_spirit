"""Contain the managers for the models in app ``preorders``."""

from django.db import models


class ShoppingCartManager(models.Manager):
    """Manage the model ``ShoppingCart``."""
    pass


class ShoppingCartLineManager(models.Manager):
    """Manage the model ``ShoppingCartLine``."""
    pass
